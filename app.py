from flask import Flask,request,Response
from botbuilder.core import BotFrameworkAdapter,BotFrameworkAdapterSettings,TurnContext,ConversationState,MemoryStorage
from botbuilder.schema import Activity
import asyncio
from pic_button import SampleAnimationCard


app = Flask(__name__)
loop = asyncio.get_event_loop()

botsettings = BotFrameworkAdapterSettings("bb4123bc-bd6f-4cfd-b596-aab3670ae1b1","76b0d7d3-7efb-4ed7-bfe2-dc7aca75e66e")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = SampleAnimationCard()


#@app.route("/api/messages",methods=["POST"])
app = web.Application(middlewares=[aiohttp_error_middleware])
app.router.add_post("/api/messages", messages)
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status = 415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity,auth_header,call_fun)
        )
    loop.run_until_complete(task)


if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error: 
        raise error
        
