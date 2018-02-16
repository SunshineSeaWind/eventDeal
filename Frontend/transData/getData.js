var fs=require('fs');
var path = require('path');


var createGraph = require('ngraph.graph');
var saveGraph = require('ngraph.tobinary');

var createLayout = require('ngraph.offline.layout');

var graph = createGraph();
var layout;


//保存所有节点，数组下标为ID
var nodes=[];
//保存所有边
var links=[] ;
var linkcount=0;

//读取文件
function readFile(fname)
{
      var readFile=JSON.parse(fs.readFileSync( fname));


      var LinkedArraySize=readFile.LinkedArraySize;
      var i=0,j=0;
      for (i=1;i<=LinkedArraySize;i++){
        //j获取LinkedArray
          var LinkedArray=readFile["LinkedArray_"+i];
          var nodeSize=LinkedArray.nodeSize

          //console.log(nodeSize);

          for(j=1;j<=nodeSize;j++){
              //获取node
              var node=LinkedArray["node_"+j];
              nodes[node.ID]=node.nodeName;
              //console.log(nodes[node.ID]);
          }
          //保存Lnik
          if(nodeSize>=2){
                for(var n=0;n<nodeSize-1;n++){
                    for(var m=n+1;m<nodeSize;m++){
                        var link=[];
                        link[0]=LinkedArray.AllNodeNameArray[n];
                        link[1]=LinkedArray.AllNodeNameArray[m];
                        links[linkcount]=link;
                        //console.log(links[linkcount][0]+"----"+links[linkcount][1]);

                        linkcount++;
                    }

                }

          }
      }

}


//遍历文件夹
function ls(ff)
{
    var files=fs.readdirSync(ff);
    for(fn in files)
    {
        var fname = ff+path.sep+files[fn];
        var stat = fs.lstatSync(fname);
        if(stat.isDirectory() == true)
        {
            ls(fname);
        }
        else
        {
            //console.log(fname);

            //读取文件
            readFile(fname)
        }
    }
}


//添加所有节点和边
function addNodes(){
  var i=0;
  for(node in nodes){
    graph.addNode(nodes[i]);
    //console.log(i+"\t"+nodes[i]);
    i++;
  }

  i=0;
  console.log("linkcount: "+linkcount);
  for(link in links){
    graph.addLink(links[i][0], links[i][1]);
    //console.log(i+"\t"+links[i][0]+"----"+links[i][1]);
    i++;
  }

}

//输出结果
function getResult(){

  saveGraph(graph, {
    outDir:'./result'
  });

  layout = createLayout(graph, {
  iterations: 1, 
  saveEach: 10, // Save each `10th` iteration
  outDir: './result', // Save results into `./myFolder`
  layout: require('ngraph.forcelayout3d') // use custom layouter
});


  layout.run(true);

}

//遍历文件夹
ls('.\\data\\official');


//添加所有节点和边
addNodes();


//输出结果
getResult();
