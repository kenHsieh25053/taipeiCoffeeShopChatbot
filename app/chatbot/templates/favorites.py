FAVORITE_MESSAGE = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [{
            "type": "text",
            "text": "最愛清單",
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
                "label": "移除店家",
                "data": "deleteshop"
            },
            "flex": 2,
            "color": "#D24444FF",
            "style": "primary"
        }]
    }
}
