flow_1 = {
    "intent": "product_info",
    "entities": [
        {"entity": "product", "prompt": "can you please enter what are you searching ?"},
        {"entity": "location", "prompt": "Please enter your location ?"}
    ],
    "api_data": {
        "url": "https://rasatest.free.beeceptor.com/"
    }
}
flow_2 = {
    "intent": "ask_price",
    "entities": [
        {"entity": "product", "prompt": "can you please enter what are you searching ?"},
        {"entity": "location", "prompt": "Please enter your location ?"}
    ],
    "api_data": {
        "url": "https://rasatest.free.beeceptor.com/"
    }
}
# {
#    					"entity": "many_sites",
#    					"prompt": "which platform"
#    				},
# 				{
#    					"entity": "register",
#    					"prompt": "Please enter what are you want to register to foodwatch platform?"
#    				},{
#    					"entity": "company",
#    					"prompt": "Please enter ?"
#    				},
flow_3 = {
    "intent": "ask_price",
    "entities": [
        {"entity": "order_id", "prompt": "Please enter your order id ?"}
    ],
    "api_data": {
        "url": "https://rasatest.free.beeceptor.com/"
    }
}