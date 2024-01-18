story_object_skeleton = {
    "title": None,
    "description": None,
    "arcs": [
        {
            "arcId": "arc1",
            "title": None,
            "description": None,
            "quests": [
                {
                    "questId": "quest1_arc1",
                    "title": None,
                    "acts": [
                        {
                            "actId": "act1_quest1_arc1",
                            "title": None,
                            "objectives": [None, None, None]  # 3 objectives
                        },
                        {
                            "actId": "act2_quest1_arc1",
                            "title": None,
                            "objectives": [None, None, None, None]  # 4 objectives
                        },
                        {
                            "actId": "act3_quest1_arc1",
                            "title": None,
                            "objectives": [None, None, None, None, None]  # 5 objectives
                        }
                    ]
                },
                # ... 4 more quests for arc1 ...
            ]
        },
        {
            "arcId": "arc2",
            "title": None,
            "description": None,
            "quests": [
                {
                    "questId": "quest1_arc2",
                    "title": None,
                    "acts": [
                        {
                            "actId": "act1_quest1_arc2",
                            "title": None,
                            "objectives": [None, None, None]  # 3 objectives
                        },
                        {
                            "actId": "act2_quest1_arc2",
                            "title": None,
                            "objectives": [None, None, None, None]  # 4 objectives
                        },
                        {
                            "actId": "act3_quest1_arc2",
                            "title": None,
                            "objectives": [None, None, None, None, None]  # 5 objectives
                        }
                    ]
                },
                # ... 4 more quests for arc2 ...
            ]
        }
    ],
    "cast": [
        # Character details (placeholders)
        {"characterId": "char1", "name": None, "role": None, "description": None},
        # ... Additional characters ...
    ],
    "currentState": {
        "currentArcId": None,
        "currentQuestId": None,
        "currentActId": None,
        "goalStatuses": {}
    }
}

# Note: Additional quests and acts for each arc should follow the same structure.

            

observations_object = {
    "location": "",
    "people": [
        {
            "name": "",
            "avatar_image": "",
            "mood": "",
            "class": "",
            "abilities": "",
            "relationship_score": 0
        }
    ],
    "actions": [
        "","",""
    ]
}

objective_object = {
    "objective_id":"",
    "name": "",
    "arcs":{},
    "quests":{},
    "acts":{}
}