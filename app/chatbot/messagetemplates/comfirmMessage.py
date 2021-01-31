COMFIRM_MESSAGE = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [{
            "type": "text",
            "text": "",
            "weight": "bold",
            "size": "xl",
            "align": "center",
            "wrap": True,
            "contents": []
        }]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [{
            "type": "button",
            "action": {
                "type": "postback",
                "label": "確定刪除",
                "data": ""
            },
            "color": "#D24444FF",
            "style": "primary"
        }]
    }
}
