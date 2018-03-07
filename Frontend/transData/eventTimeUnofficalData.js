var fs=require('fs');
var path = require('path');


var createGraph = require('ngraph.graph');
var saveGraph = require('ngraph.tobinary');

// var createLayout = require('ngraph.offline.layout');

var graph = createGraph();
var layout;


//保存所有节点，数组下标为ID
var nodes=[];
var timeNodes=[];   //timenode
//保存所有边
var links=[] ;
var linkcount=0;

//读取文件
function readFile(fname)
{
      var readFile=JSON.parse(fs.readFileSync(fname));


      var LinkedArraySize=readFile.LinkedArraySize;

      timeNodes.push(readFile.Date);
      var tmpnode=[];

      var i=0,j=0;
      for (i=1;i<=LinkedArraySize;i++){
          var node=readFile["LinkedArray_"+i];
          var Obj=new Object();
          Obj.keywords = node.keywords.join(' ')
          Obj.data = node.AllNodeNameArray.join(' ')
          // nodes.push(node.keywords.join(' '));
          // tmpnode.push(node.keywords.join(' '));
          nodes.push(Obj);
          tmpnode.push(Obj.keywords);
      }

      //creat link
      for (iter in tmpnode){
          var link = [];
          link[0]=timeNodes[timeNodes.length-1];
          link[1]=tmpnode[j];
          links[linkcount]=link;
          j++;
          linkcount++;
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
    // graph.addNode(nodes[i]);
    graph.addNode(nodes[i].keywords,nodes[i].data);
    //console.log(i+"\t"+nodes[i]);
    i++;
  }

  i = 0;

  for(node in timeNodes){
    graph.addNode(timeNodes[i]);
    //console.log(i+"\t"+timeNodes[i]);
    i++;
  }

  // 在时间节点之间添加link关系
  i = 0;
  for(node in timeNodes){
    if (i < timeNodes.length - 1){
      for(var j = 0 ; j < 50 ; j++){
        graph.addLink(timeNodes[i], timeNodes[i+1]);
      }
    }
    i++;
  }

  i = 0;
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
    outDir:'./UnofficialTimeline'
  });

//   layout = createLayout(graph, {
//   iterations: 100,
//   saveEach: 10, // Save each `10th` iteration
//   outDir: './UnofficialTimeline', // Save results into `./myFolder`
//   layout: require('ngraph.forcelayout3d') // use custom layouter
// });


  // layout.run(true);

}

//遍历文件夹
ls('D:\\F\\FengRuCup\\Ring大数据-中印对峙爬虫数据\\数据\\result\\unofficial');


//添加所有节点和边
addNodes();


//输出结果
getResult();
