import sys
import uvicorn
from graph import build_graph

def cli():
    graph=build_graph()
    result = graph.invoke({"topic":"EV markets between India and US"})
    print(f"Final_Report:{result}")

def run_api():
    uvicorn.run("app:app",host="127.0.0.1", port=8000,reload=True) #local testing
  #  uvicorn.run("app:app",host="0.0.0.0", port=8000,reload=True)  #production



if __name__ =="__main__":
    if (len(sys.argv))>1 and sys.argv[1]=="api":
        run_api()
    else:
        cli()


 
