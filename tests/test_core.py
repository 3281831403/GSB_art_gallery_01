import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_register(self):
        state = core.new_game()
        self.assertTrue(core.register(state, "E1"))
        self.assertFalse(core.register(state, "E1"))

    def test_02_hall_capacity(self):
        state = core.new_game()
        core.place(state, "E1")
        core.place(state, "E2")
        result = core.place(state, "E3")
        self.assertFalse(result)

    def test_03_fee_exact(self):
        state = core.new_game()
        self.assertEqual(core.fee(state, "E1", 3), 2)

    def test_04_cancel_refunds_deposit(self):
        state = core.new_game()
        state["deposit"] = 80
        core.cancel(state, "E1")
        self.assertEqual(state["deposit"], 100)

    def test_05_no_assign_absent_guide(self):
        state = core.new_game()
        core.register(state, "E1")
        result = core.assign(state, "E1", "G2")
        self.assertFalse(result)

    def test_06_setup_fail_no_cost(self):
        state = core.new_game()
        core.register(state, "E1")
        state["exhibits"]["E1"]["failed"] = True
        before = state["deposit"]
        result = core.setup(state, "E1")
        self.assertFalse(result)
        self.assertEqual(state["deposit"], before)

    def test_07_damage_once(self):
        state = core.new_game()
        core.register(state, "E1")
        core.damage(state, "E1")
        self.assertEqual(state["exhibits"]["E1"]["health"], 90)

    def test_08_load_preserves_exhibit(self):
        state = core.new_game()
        state["exhibit_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["exhibit_id"], 4)


if __name__ == "__main__":
    unittest.main()
