var createGraph = require('ngraph.graph');
var saveGraph = require('ngraph.tobinary');

var graph = createGraph();
for (var i = 0; i < 100; i++) {
  graph.addNode(i, 'test');
}
for (i = 0; i < 99; i++) {
  graph.addLink(i, i + 1);
}
console.log('Node count:', graph.getNodesCount());
console.log('Link count:', graph.getLinksCount());
saveGraph(graph, {
  outDir:'./temp'
});
