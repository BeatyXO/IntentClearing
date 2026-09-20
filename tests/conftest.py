# The pinned gltest loader injects the GenLayer message by dup2'ing a temporary
# file over stdin, then immediately unlinks it. Windows refuses to unlink an
# open stdin file, so preserve the exact loader behavior through contract import
# and restore stdin before deleting the temporary file.
import os
import sys


def pytest_configure():
    from gltest.direct.vm import VMContext

    original_refresh_gl_message = VMContext._refresh_gl_message

    def refresh_gl_message_with_timestamp(vm):
        original_refresh_gl_message(vm)
        gl_module = sys.modules.get("genlayer.gl")
        raw_message = getattr(gl_module, "message_raw", None) if gl_module else None
        if isinstance(raw_message, dict):
            raw_message["datetime"] = vm._datetime

    VMContext._refresh_gl_message = refresh_gl_message_with_timestamp

    if os.name != "nt":
        return

    from gltest.direct import loader

    original_load_contract_class = loader.load_contract_class

    def windows_safe_load_contract_class(contract_path, vm, sdk_version=None):
        deferred_unlinks = []
        actual_unlink = os.unlink

        def defer_only_open_stdin_file(path, *args, **kwargs):
            try:
                return actual_unlink(path, *args, **kwargs)
            except PermissionError as error:
                if getattr(error, "winerror", None) != 32:
                    raise
                deferred_unlinks.append(path)

        os.unlink = defer_only_open_stdin_file
        try:
            return original_load_contract_class(contract_path, vm, sdk_version)
        finally:
            os.unlink = actual_unlink
            original_stdin_fd = getattr(vm, "_original_stdin_fd", None)
            if original_stdin_fd is not None:
                os.dup2(original_stdin_fd, 0)
                os.close(original_stdin_fd)
                vm._original_stdin_fd = None
            for path in deferred_unlinks:
                actual_unlink(path)

    loader.load_contract_class = windows_safe_load_contract_class
