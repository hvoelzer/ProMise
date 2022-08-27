<template>
    <div>
        <h1>Graph View</h1>
        <svg width="100%" height="100" id="mainSvg">
        </svg>
    </div>
</template>

<script>
import router from '@/router';

export default {
  name: 'App',
  props: ['selected'],

  data(){
    return{
        edges: {},
        svgElementsToRemove: [],
        selectedNode: this.selected,
        delay: 500,
        clicks: 0,
        timer: null
    }
  },
  methods: {
    getGraph(){
      try {
        this.axios.get(this.$backend.getGraph())
        .then((json) => {
        
          this.edges = json.data;
          this.drawGraph()
          
          console.log("GET GRAPH SUCCEEDED");
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
      if (node1 != node2){   // TODO at some point address selfloops
        var mainSvg = document.getElementById('mainSvg');
        var edge;
        var label;
        var arrowpoint;
        var parentNode = document.getElementById(node1);
        var childNode = document.getElementById(node2);
        var xParent = parseFloat(parentNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth();
        var yParent = parentNode.getAttribute("cy");
        var xChild = parseFloat(childNode.getAttribute("cx").replace("%", '')) / 100 * this.getWidth();
        var yChild = childNode.getAttribute("cy");
        var hypotenuse = Math.sqrt(
              Math.pow(parseFloat(xChild - xParent) , 2) +
              Math.pow(parseFloat(yChild - yParent) , 2)
              )
        var xFixParent = 50 / hypotenuse  * parseFloat(xChild - xParent);
        var yFixParent = 50 / hypotenuse  * parseFloat(yChild - yParent);
        var xFixChild = 50 / hypotenuse  * parseFloat(xParent - xChild);
        var yFixChild = 50 / hypotenuse  * parseFloat(yParent - yChild);

        xParent = parseFloat(xParent) + parseFloat(xFixParent) - 7;
        yParent = parseFloat(yParent) + parseFloat(yFixParent);
        xChild = parseFloat(xChild) + parseFloat(xFixChild) - 7;
        yChild = parseFloat(yChild) + parseFloat(yFixChild);


        edge = document.createElementNS("http://www.w3.org/2000/svg", "path");
        edge.setAttribute("d", "M " + xParent + " " + yParent + " L" + xChild + " " + yChild);
        edge.setAttribute("stroke", "red");
        edge.setAttribute("stroke-width", "3");
        
        var x = parseFloat(parseFloat(xParent) + parseFloat(xChild - xParent) / 2)
        var y = parseFloat(parseFloat(yParent) + parseFloat(yChild - yParent) / 2)
        label = document.createElementNS("http://www.w3.org/2000/svg", "text");
        label.setAttribute("x", x);
        label.setAttribute("y", y);
        label.setAttribute("text-anchor", "middle");
        label.textContent = operation;

        mainSvg.appendChild(edge);
        mainSvg.appendChild(label);

        this.svgElementsToRemove.push(edge)
        this.svgElementsToRemove.push(label)

        var newHypotenuse = Math.sqrt(
              Math.pow(parseFloat(xChild - xParent) , 2) +
              Math.pow(parseFloat(yChild - yParent) , 2)
              )
        var distance = 15;
        var xArrowBase = (distance * Math.sqrt(2)/2) / newHypotenuse  * parseFloat(xParent - xChild);
        var yArrowBase = (distance * Math.sqrt(2)/2) / newHypotenuse  * parseFloat(yParent - yChild);
        xArrowBase = parseFloat(xChild) + parseFloat(xArrowBase);
        yArrowBase = parseFloat(yChild) + parseFloat(yArrowBase);
        var centerBasex = parseFloat(xChild) + parseFloat(distance / 2);
        var centerBasey = parseFloat(yChild) + parseFloat(distance / 2);
        var w = Math.sqrt(Math.pow((centerBasex - xArrowBase), 2) + Math.pow((centerBasey - yArrowBase), 2))
        var cosAngle = 1 - (Math.pow(w, 2) / (2 * Math.pow((distance * Math.sqrt(2)/2), 2)))
        var sinAngle = Math.sqrt( 1 - Math.pow(cosAngle, 2))

        var point2xI = distance
        var point2yI = 0
        var point3xI = 0
        var point3yI = distance

        var point2x
        var point2y
        var point3x
        var point3y

        if (parseFloat(xParent - xChild) >= 0){
          
          point2x = parseFloat(point2xI) * parseFloat(sinAngle) + parseFloat(point2yI) * parseFloat(cosAngle)
          point2y = parseFloat(point2xI) * parseFloat(cosAngle) - parseFloat(point2yI) * parseFloat(sinAngle)
          
          point3x = parseFloat(point3xI) * parseFloat(sinAngle) + parseFloat(point3yI) * parseFloat(cosAngle)
          point3y = parseFloat(point3xI) * parseFloat(cosAngle) - parseFloat(point3yI) * parseFloat(sinAngle)
        }
        else{
          point2y = parseFloat(point2xI) * parseFloat(sinAngle) + parseFloat(point2yI) * parseFloat(cosAngle)
          point2x = parseFloat(point2xI) * parseFloat(cosAngle) - parseFloat(point2yI) * parseFloat(sinAngle)
          
          point3y = parseFloat(point3xI) * parseFloat(sinAngle) + parseFloat(point3yI) * parseFloat(cosAngle)
          point3x = parseFloat(point3xI) * parseFloat(cosAngle) - parseFloat(point3yI) * parseFloat(sinAngle) 
        }

        point2x = parseFloat(xChild) + parseFloat(point2x)
        point2y = parseFloat(yChild) + parseFloat(point2y)
        point3x = parseFloat(xChild) + parseFloat(point3x)
        point3y = parseFloat(yChild) + parseFloat(point3y)

        arrowpoint = document.createElementNS("http://www.w3.org/2000/svg", "path");
        arrowpoint.setAttribute("d", "M " + xChild + " " + yChild + " L" + point2x + " " + point2y + " L" + point3x + " " + point3y + "Z");
        arrowpoint.setAttribute("stroke", "red");
        arrowpoint.setAttribute("fill", "red");
        arrowpoint.setAttribute("stroke-width", "3");

        mainSvg.appendChild(arrowpoint);
        this.svgElementsToRemove.push(arrowpoint)
      }  
    },
    postChangeOfLog(id){
      
      try {
          this.axios.post(this.$backend.changeSelectedNode(), {"id":id})
          .then(() => {
              console.log("CHANGE SELECTED ID IN BACKEND");
          })
      }
      catch (e) {
          console.log(e);
      }
  
    },
    changeLog(id){
      this.clicks++;
      var oldSelectedNode = document.getElementById(this.selectedNode);
      oldSelectedNode.setAttribute("fill", "blue")
      this.selectedNode = id
      var newSelectedNode = document.getElementById(this.selectedNode);
      newSelectedNode.setAttribute("fill", "aqua")
      this.$emit('changeSelected', id)
      this.postChangeOfLog(id)
      if (this.clicks === 1) {
        this.timer = setTimeout( () => {
          this.clicks = 0;
        }, this.delay);
      } else {
        clearTimeout(this.timer);  
        router.push("/app/filter");
        this.clicks = 0;
      }   
    },
    toFilterView(id){
      console.log(id)
    },
    drawNode(x, y, id){
      var mainSvg = document.getElementById('mainSvg');
      var circle;
      var label

      circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", x + "%");
      circle.setAttribute("cy", y + "");
      circle.setAttribute("r",  50);
      circle.setAttribute("fill", (this.selectedNode == id) ? 'aqua' : 'blue');
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
      var layerHeight = 100
      var betweenLayersHeight = 60
      // draw Nodes
      for(var level in this.edges.levels){
          var nNodesInRow = this.edges.levels[level].nodes.length
          for(var node in this.edges.levels[level].nodes){
              this.drawNode(100 /  (nNodesInRow + 1) * (parseFloat(node) + 1) , (layerHeight + betweenLayersHeight) * (parseFloat(level) + 1), this.edges.levels[level].nodes[node]);  
          }
      }
      var nLevels = this.edges.levels.length
      document.getElementById('mainSvg').setAttribute("height", layerHeight + ((layerHeight + betweenLayersHeight) * nLevels)); 

      // draw Edges
      this.drawEdges()
    },
    drawEdges(){
      this.removeOldEdges()
      for(var edge in this.edges.edges){
        this.drawEdge(this.edges.edges[edge].parentNode, this.edges.edges[edge].operation, this.edges.edges[edge].childrenNode)
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