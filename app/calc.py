from app import database


def run_inefficient(db, team):
    all_types = database.get_all_names(db, 'types')

    results = []
    for enemy_type in all_types:  # each possible enemy type
        team_results = [enemy_type]
        for poke in team:
            # remove name and type2s that are empty strings
            types = list(filter(lambda elem: elem, poke[1:]))
            poke_type = '_'.join(types)
            offense = list(
                database.get_damage(db, o, enemy_type) for o in types)
            enemy_types = enemy_type.split('_')
            defense = list(
                database.get_damage(db, o, poke_type) for o in enemy_types)
            team_results.append(max(offense) / max(defense))
        team_score = sum(team_results[1:])
        team_results.insert(0, team_score)
        results.append(team_results)

    return results
