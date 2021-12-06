# mindmap
REST API create a mind map and store its data

#Setup
Require python module:
  - falsk
  - marshmallow
  - webargs
  - request

#Start API
 ./bin/run.sh
 .\bin\run.bat

#Create a mind map
curl -X POST -H "Content-Type: application/json" -d "{\"id\": \"my-map\"}" http://127.0.0.1:8081/createmap

#Add a leaf (path) to the map
curl -X POST -H "Content-Type: application/json" -d "{\"path\": \"i\/like\/potatoes\",\"text\": \"Because I like it\"}" http://localhost:8081/addleaf?id=my-map

#Read a leaf (path) of the map
curl -X GET -H "Content-Type: application/json" "http://localhost:8081/readleaf?id=my-map&path=i/like/potatoes"

#Read the whole tree of the mind map
curl -X GET -H "Content-Type: application/json" "http://localhost:8081/readmap?id=my-map"

Docker Support

build docker image
  docker build --tag api-mindmap .

Run docker
  docker run --name=api-mindmap -d -v <localpath>:/app/data -p 8081:8081 api-mindmap



