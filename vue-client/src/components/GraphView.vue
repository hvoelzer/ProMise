<template>
    <div>
        <h1> I am the Graph View</h1>
        <svg width="100%" height="100" id="mainSvg">
        </svg>
    </div>
</template>

<script>
export default {
  name: 'App',

  data(){
    return{
        edges: {},
        svgElementsToRemove: []
    }
  },
  methods: {
    getGraph(){
        try {
            this.axios.get(this.$backend.getGraph())
            .then((json) => {
            //console.log(json.data)
            this.edges = json.data;
            this.drawGraph()
            //this.$forceUpdate();
            console.log("SUCCESS");
            })
        }
        catch (e) {
            console.log(e);
        }
    },
    getWidth() {
      return Math.max(
        document.body.scrollWidth,
        document.documentElement.scrollWidth,
        document.body.offsetWidth,
        document.documentElement.offsetWidth,
        document.documentElement.clientWidth
      );
    },
    drawEdge(node1, operation, node2){
      var mainSvg = document.getElementById('mainSvg');
      var edge;
      var label;
      var parentNode = document.getElementById(node1);
      var childNode = document.getElementById(node2);
      var xParent = parseInt(parentNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth();
      var yParent = parentNode.getAttribute("cy");
      var xChild = parseInt(childNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth();
      var yChild = childNode.getAttribute("cy");
      var hypotenuse = Math.sqrt(
            Math.pow(parseInt(xChild - xParent) , 2) +
            Math.pow(parseInt(yChild - yParent) , 2)
            )
      console.log(hypotenuse)

      edge = document.createElementNS("http://www.w3.org/2000/svg", "path");
      console.log("M " + xParent + " " + yParent + " l " + xChild + " " + yChild)
      edge.setAttribute("d", "M " + xParent + " " + yParent + " L" + xChild + " " + yChild);
      edge.setAttribute("stroke", "red");
      edge.setAttribute("stroke-width", "3");
      
      var x = parseInt(parseInt(xParent) + parseInt(xChild - xParent) / 2)
      var y = parseInt(parseInt(yParent) + parseInt(yChild - yParent) / 2)
      label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", x);
      label.setAttribute("y", y);
      label.setAttribute("text-anchor", "middle");
      label.textContent = operation;

      mainSvg.appendChild(edge);
      mainSvg.appendChild(label);

      this.svgElementsToRemove.push(edge)
      this.svgElementsToRemove.push(label)
    },
    changeLog(id){
      console.log(id);
    },
    drawNode(x, y, id){
      var mainSvg = document.getElementById('mainSvg');
      var circle;
      var label

      circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", x + "%");
      circle.setAttribute("cy", y + "");
      circle.setAttribute("r",  50);
      circle.setAttribute("fill", "blue");
      circle.setAttribute("stroke", "black");
      circle.setAttribute("id", id);
      circle.addEventListener ("click", this.changeLog.bind(null, id), false);

      label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", x + "%");
      label.setAttribute("y", y + "");
      label.setAttribute("text-anchor", "middle");
      label.textContent = id

      mainSvg.appendChild(circle);
      mainSvg.appendChild(label);

    },
    drawGraph(){
      // draw Nodes
      for(var level in this.edges.levels){
          var nNodesInRow = this.edges.levels[level].nodes.length
          for(var node in this.edges.levels[level].nodes){
              this.drawNode(100 /  (nNodesInRow + 1) * (parseInt(node) + 1) , 140 * (parseInt(level) + 1), this.edges.levels[level].nodes[node]);  
          }
      }
      var nLevels = this.edges.levels.length
      document.getElementById('mainSvg').setAttribute("height", 100 + (140 * nLevels)); 

      // draw Edges
      this.drawEdges()
    },
    drawEdges(){
      this.removeOldEdges()
      for(var edge in this.edges.edges){
        this.drawEdge(this.edges.edges[edge].parentNode, this.edges.edges[edge].operation, this.edges.edges[edge].childrenNode)
        console.log(this.edges.edges[edge])
      }
    },
    removeOldEdges(){
      for(var element in this.svgElementsToRemove){
        document.getElementById('mainSvg').removeChild(this.svgElementsToRemove[element]);
      }
      this.svgElementsToRemove = [];
    }
  },
  mounted(){
    this.getGraph();
    window.addEventListener('resize', this.drawEdges)
  }

}
</script>