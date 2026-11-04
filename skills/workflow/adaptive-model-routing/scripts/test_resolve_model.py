import unittest
from resolve_model import RoutingError, check, resolve


class ResolverTests(unittest.TestCase):
    def inventory(self, *models):
        return {'models': [{'id': model} if isinstance(model, str) else model for model in models]}

    def test_current_runtime_resolves_new_sol(self):
        available = self.inventory('gpt-5.6-sol', 'gpt-6-sol', 'gpt-6.1-sol', 'gpt-6-astra', 'gpt-6-luna', 'gpt-9-terra')
        self.assertEqual(resolve(available, 'sol')['model'], 'gpt-6.1-sol')

    def test_exclusions_cover_explicit_inherited_and_fallback_checks(self):
        for model in ('gpt-6-sol', 'gpt-6.0-sol', 'gpt-6.0.2-sol'):
            with self.subTest(model=model), self.assertRaises(RoutingError):
                check(self.inventory(model), model)
        with self.assertRaises(RoutingError):
            resolve(self.inventory('gpt-6-sol', 'gpt-6.0-sol'), 'sol')

    def test_terra_resolution_and_preflight_use_latest_stable_release(self):
        inventory = self.inventory('gpt-6-terra', 'gpt-6.1-terra',
                                   {'id': 'gpt-7-terra', 'status': 'preview'})
        self.assertEqual(resolve(inventory, 'terra')['model'], 'gpt-6.1-terra')
        self.assertEqual(check(inventory, 'gpt-6.1-terra')['model'], 'gpt-6.1-terra')
        with self.assertRaises(RoutingError):
            check(inventory, 'gpt-6-terra')

    def test_new_versions_need_no_policy_edit_and_sort_numerically(self):
        self.assertEqual(resolve(self.inventory('gpt-6.9-sol', 'gpt-6.10-sol'), 'sol')['model'], 'gpt-6.10-sol')
        self.assertEqual(resolve(self.inventory('gpt-6.10-sol', 'gpt-7-sol'), 'sol')['model'], 'gpt-7-sol')

    def test_no_guessed_alias_or_stale_inheritance(self):
        for model in ('sol-latest', 'gpt-sol-latest', 'gpt-6-sol-2026-10-01'):
            with self.subTest(model=model), self.assertRaises(RoutingError):
                resolve(self.inventory(model), 'sol')
        with self.assertRaises(RoutingError):
            check(self.inventory('gpt-6.1-sol', 'gpt-6.2-sol'), 'gpt-6.1-sol')

    def test_release_availability_and_old_descriptions(self):
        blocked = [{'id': 'gpt-7-sol', 'status': 'preview'},
                   {'id': 'gpt-8-sol', 'available': False},
                   {'id': 'gpt-9-sol', 'description': 'Older generation model'},
                   {'id': 'gpt-10-sol', 'description': 'Experimental release'}]
        self.assertEqual(resolve(self.inventory('gpt-6.1-sol', *blocked), 'sol')['model'], 'gpt-6.1-sol')
        with self.assertRaises(RoutingError):
            resolve(self.inventory(*blocked), 'sol')

    def test_ambiguity_blocks_instead_of_guessing(self):
        with self.assertRaises(RoutingError):
            resolve(self.inventory('gpt-6.1-sol', 'gpt-6.1.0-sol'), 'sol')
        with self.assertRaises(RoutingError):
            resolve(self.inventory({'id': 'gpt-6.1-sol', 'is_latest': True}, 'gpt-6.2-sol'), 'sol')

    def test_does_not_invent_reasoning_defaults(self):
        self.assertIsNone(resolve(self.inventory('gpt-6.1-sol'), 'sol')['default_reasoning_effort'])
        inventory = self.inventory({'id': 'gpt-6.1-sol', 'default_reasoning_effort': 'low', 'supported_reasoning_efforts': ['low', 'high']})
        self.assertEqual(resolve(inventory, 'sol')['default_reasoning_effort'], 'low')

    def test_newest_marked_not_latest_blocks_resolution_and_preflight(self):
        for older_marker in (True, False, None):
            older = {'id': 'gpt-6.1-sol'}
            if older_marker is not None:
                older['is_latest'] = older_marker
            inventory = self.inventory(older, {'id': 'gpt-6.2-sol', 'is_latest': False})
            with self.subTest(older_marker=older_marker):
                with self.assertRaises(RoutingError):
                    resolve(inventory, 'sol')
                for model in ('gpt-6.1-sol', 'gpt-6.2-sol'):
                    with self.assertRaises(RoutingError):
                        check(inventory, model)

    def test_conflicting_duplicates_block_before_eligibility_filtering(self):
        for metadata in ({'available': False}, {'status': 'preview'},
                         {'is_latest': False}, {'description': 'Older generation model'}):
            eligible = {'id': 'gpt-6.2-sol', 'available': True, 'status': 'stable',
                        'is_latest': True, 'description': 'Latest model'}
            conflicting = {**eligible, **metadata}
            for entries in ((eligible, conflicting), (conflicting, eligible)):
                inventory = self.inventory(*entries)
                with self.subTest(metadata=metadata, entries=entries):
                    with self.assertRaises(RoutingError):
                        resolve(inventory, 'sol')
                    with self.assertRaises(RoutingError):
                        check(inventory, eligible['id'])

    def test_consistent_latest_markers_and_identical_duplicates_are_accepted(self):
        newest = {'id': 'gpt-6.2-sol', 'is_latest': True}
        inventory = self.inventory({'id': 'gpt-6.1-sol', 'is_latest': False}, newest, newest.copy())
        self.assertEqual(resolve(inventory, 'sol')['model'], newest['id'])
        self.assertEqual(check(inventory, newest['id'])['model'], newest['id'])

    def test_other_families_resolve_independently(self):
        inventory = self.inventory('gpt-6-astra', 'gpt-6.1-astra', 'gpt-6-luna')
        self.assertEqual(resolve(inventory, 'astra')['model'], 'gpt-6.1-astra')
        self.assertEqual(resolve(inventory, 'luna')['model'], 'gpt-6-luna')


if __name__ == '__main__':
    unittest.main()
