# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

"""Minimal consumer proving an IntentClearing fill can gate another IC action."""

from genlayer import *
from dataclasses import dataclass


@gl.contract_interface
class IIntentClearing:
    class View:
        def is_fill_valid(self, fill_id: u256, expected_market_hash: str, expected_epoch_hash: str, expected_fill_hash: str) -> bool: ...
        def is_fill_party(self, fill_id: u256, expected_market_hash: str, expected_epoch_hash: str, expected_fill_hash: str, actor: Address) -> bool: ...
    class Write:
        pass


@allow_storage
@dataclass
class Consumption:
    fill_id: u256
    actor: Address
    market_hash: str
    epoch_hash: str
    fill_hash: str
    action_hash: str


class ClearingGate(gl.Contract):
    clearing_address: Address
    consumed: TreeMap[str, Consumption]
    fill_party_index: TreeMap[str, str]
    consumption_count: u256

    def __init__(self, clearing_address: Address):
        self.clearing_address = clearing_address
        self.consumption_count = u256(0)

    @gl.public.write
    def consume_fill(self, fill_id: u256, expected_market_hash: str, expected_epoch_hash: str, expected_fill_hash: str, action_hash: str) -> None:
        market_hash = str(expected_market_hash).strip().lower()
        epoch_hash = str(expected_epoch_hash).strip().lower()
        fill_hash = str(expected_fill_hash).strip().lower()
        action = str(action_hash).strip().lower()
        for field, value in (("market_hash", market_hash), ("epoch_hash", epoch_hash), ("fill_hash", fill_hash), ("action_hash", action)):
            if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise gl.vm.UserError(f"EXPECTED: {field} must be a 32-byte lowercase hex digest")
        if action in self.consumed:
            raise gl.vm.UserError("EXPECTED: action hash already consumed")
        clearing = IIntentClearing(self.clearing_address)
        if not clearing.view().is_fill_valid(fill_id, market_hash, epoch_hash, fill_hash):
            raise gl.vm.UserError("EXPECTED: fill does not match pinned market/epoch/fill hash")
        actor = gl.message.sender_address
        if not clearing.view().is_fill_party(fill_id, market_hash, epoch_hash, fill_hash, actor):
            raise gl.vm.UserError("EXPECTED: caller is not a party to the fill")
        party_key = str(int(fill_id)) + ":" + str(actor).lower()
        if party_key in self.fill_party_index:
            raise gl.vm.UserError("EXPECTED: this fill was already consumed by this party")
        self.consumed[action] = Consumption(fill_id=fill_id, actor=actor, market_hash=market_hash, epoch_hash=epoch_hash, fill_hash=fill_hash, action_hash=action)
        self.fill_party_index[party_key] = action
        self.consumption_count = u256(int(self.consumption_count) + 1)

    @gl.public.view
    def was_consumed(self, action_hash: str) -> bool:
        return str(action_hash).strip().lower() in self.consumed
