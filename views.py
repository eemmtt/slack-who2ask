#slack ui views
from dbops import *
from admincheck import *
from dotenv import load_dotenv
import os
load_dotenv()

WORKSPACE = os.environ["WORKSPACE"]
def compose_home(user_name, user_image, is_admin):
    # if not is_admin:
    elements = [{
					"type": "button",
                    "action_id": "button_view_profile",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "View Profile"
					},
					"value": "View Profile",
				}]
    if is_admin:
        elements.append({
					"type": "button",
                    "action_id": "button_view_admin",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "View Admin"
					},
					"value": "View Admin",
				})
        
    view = {
        "type": "home",
        "blocks": [
            {
			"type": "actions",
			"elements": elements
		    },
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "input_search",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "[Topic Name]"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": ":mag: Search ",
                    "emoji": True
                }
            }
        ]
    }
    return view

def compose_search_results(query, results, is_admin):
    elements = [{
					"type": "button",
                    "action_id": "button_view_profile",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "View Profile"
					},
					"value": "View Profile",
				}]
    
    if is_admin:
        elements.append({
					"type": "button",
                    "action_id": "button_view_admin",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "View Admin"
					},
					"value": "View Admin",
				})
        
    results_formatted = [
        {
			"type": "actions",
			"elements": elements
		},
        {
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "input_search",
				"placeholder": {
					"type": "plain_text",
					"text": "[Topic Name]"
				}
			},
			"label": {
				"type": "plain_text",
				"text": ":mag: Search ",
				"emoji": True
			}
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Search results for *{query}:*"
                }
            },
            {
                "type": "divider"
            }
    ]
    
    for result in results[:10]:
        user_id = result[0]
        real_name = result[1]
        avatar = result[2]
        topic_name = result[3].title()
        topic_desc = result[4]
        com_badge = get_badge("community", result[5])
        sno_badge = get_badge("snohetta", result[6])
        results_formatted.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{topic_name}*{sno_badge}{com_badge}\n{topic_desc}\n:incoming_envelope:<https://{WORKSPACE}.slack.com/team/{user_id}|{real_name}>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": avatar,
                    "alt_text": real_name
                }
        })
        
    results_formatted.append({"type": "divider"})
    
        
    view = {
        "type": "home",
        "blocks": results_formatted
    }
    return view

def compose_profile(topics):
    #print(topics)
    topics_formatted = [
		{
			"type": "actions",
			"elements": [
                {
					"type": "button",
     				"action_id": "button_return_to_search",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Return to Search"
					},
					"value": "click_me_123"
				},
				{
					"type": "button",
					"action_id": "button_add_topic",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Add Topic"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"action_id": "button_delete_topic",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Delete Topic"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		},
  		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your Topics*"
			}
		},
		{
			"type": "divider"
		}
    ]
    
    for topic in topics:
        topic_title = topic[1]
        topic_notes = topic[2]
        topic_badge_community = topic[3]
        topic_badge_snohetta = topic[4]
        topics_formatted.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{topic_title}*\n{topic_notes}"
			},
			"accessory": {
				"type": "button",
				"action_id": "button_edit_topic",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Edit"
				},
				"value": f"{topic[0]}"
			}
		})
	
    topics_formatted.append({"type": "divider"})
    
    view = {
        "type": "home",
        "blocks": topics_formatted
    }
    return view

def compose_edit_modal(topic):
    topic_name = topic[1]
    topic_notes = topic[2]
    view = {
		"type": "modal",
  		"private_metadata": f"{topic[0]}",
		"callback_id": "topic_edit_modal",
		"title": {
			"type": "plain_text",
			"text": "My App",
			"emoji": True
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit Edit",
			"emoji": True
		},
		"close": {
			"type": "plain_text",
			"text": "Cancel",
			"emoji": True
		},
		"blocks": [
			{
				"type": "input",
				"block_id": "topic_name_field",
				"element": {
					"type": "plain_text_input",
					"action_id": "topic_name_input",
					"initial_value": f"{topic_name}",
				},
				"label": {
					"type": "plain_text",
					"text": "Topic Name",
					"emoji": True
				}
			},
			{
				"type": "input",
    			"block_id": "topic_notes_field",	
				"element": {
					"type": "plain_text_input",
					"action_id": "topic_notes_input",
					"initial_value": f"{topic_notes}",
					"multiline": True,
				},
				"label": {
					"type": "plain_text",
					"text": "Topic Notes",
					"emoji": True
				}
			}
		]
	}
    return view

def compose_add_modal():
    view = {
		"type": "modal",
		"callback_id": "topic_add_modal",
		"title": {
			"type": "plain_text",
			"text": "Add Topic",
			"emoji": True
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit",
			"emoji": True
		},
		"close": {
			"type": "plain_text",
			"text": "Cancel",
			"emoji": True
		},
		"blocks": [
			{
				"type": "input",
				"block_id": "topic_name_field",
				"element": {
					"type": "plain_text_input",
					"action_id": "topic_name_input",
					"placeholder": {
                        "type": "plain_text",
                        "text": "eg. Dealing With Spiders"
                    }
				},
				"label": {
					"type": "plain_text",
					"text": "Topic Name",
					"emoji": True
				}
			},
   			{
				"type": "input",
    			"block_id": "topic_notes_field",	
				"element": {
					"type": "plain_text_input",
					"action_id": "topic_notes_input",
					"placeholder": {
                        "type": "plain_text",
                        "text": "eg. I have developed many techniques to deal with my fear of spiders. Ask me about them!"
                    },
					"multiline": True,
				},
				"label": {
					"type": "plain_text",
					"text": "Topic Notes",
					"emoji": True
				}
			}
		]
	}
    return view

def compose_profile_delete(topics):
    #print(topics)
    topics_formatted = [
		{
			"type": "actions",
			"elements": [
                {
					"type": "button",
     				"action_id": "button_return_to_search",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Return to Search"
					},
					"value": "click_me_123"
				},
				{
					"type": "button",
					"action_id": "button_add_topic",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Add Topic"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"action_id": "button_cancel_delete_topic",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Cancel Delete"
					},
					"value": "click_me_123"
				}
			]
		},
  		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Your Topics*"
			}
		},
		{
			"type": "divider"
		}
    ]
    
    for topic in topics:
        topic_title = topic[1]
        topic_notes = topic[2]
        topic_badge_community = topic[3]
        topic_badge_snohetta = topic[4]
        topics_formatted.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{topic_title}*\n{topic_notes}"
			},
			"accessory": {
				"type": "button",
				"action_id": "button_confirm_delete_topic",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Delete"
				},
				"value": f"{topic[0]}",
    			"style": "danger",
				"confirm": {
					"title": {
						"type": "plain_text",
						"text": f"Delete '{topic_title}'?"
					},
					"text": {
						"type": "mrkdwn",
						"text": "Are you sure you want to delete this topic?"
					},
					"confirm": {
						"type": "plain_text",
						"text": "Yes, delete it!"
					},
					"deny": {
						"type": "plain_text",
						"text": "Stop, I've changed my mind!"
					}
				}
			}
		})
	
    topics_formatted.append({"type": "divider"})
    
    view = {
        "type": "home",
        "blocks": topics_formatted
    }
    return view

def compose_admin():
    view = {
		"type": "home",
		"blocks": [
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Return To Search",
							"emoji": True
						},
						"value": "click_me_123",
						"action_id": "button_return_to_search"
					}
				]
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Admin Panel*"
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Add User",
							"emoji": True
						},
						"value": "click_me_123",
						"action_id": "admin_add_user"
					},
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Remove User",
							"emoji": True
						},
						"value": "click_me_123",
						"action_id": "admin_remove_user"
					},
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Get All Users As JSON",
							"emoji": True
						},
						"value": "click_me_123",
						"action_id": "admin_get_all_users"
					}
				]
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Add Badge to Topic",
							"emoji": True
						},
						"value": "click_me_123",
						"action_id": "admin_add_badge_to_topic"
					}
				]
			}
		]
	}
    return view