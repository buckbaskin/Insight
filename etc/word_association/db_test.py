from GraphDb import Word, RelatesTo
from bulbs.neo4jserver import Graph, Config, NEO4J_URI

config = Config(NEO4J_URI)
g = Graph(config)
g.add_proxy("word", Word)
g.add_proxy("relatesTo", RelatesTo)

rob = g.word.create(name="robotics")
ali = g.people.create(name="alibaba")
g.relatesTo.create(rob, ali, tests="100", occurences="80")