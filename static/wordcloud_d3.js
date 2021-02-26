// グラフの表示設定
var margin = { top: 10, right: 10, bottom: 10, left: 10 },
	width = 450 - margin.left - margin.right,
	height = 300 - margin.top - margin.bottom;

// svgオブジェクトの追加
var svg = d3.select("#wordcloud").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform",
			"translate(" + margin.left + "," + margin.top + ")");


function draw_wordcloud(tweets_text){
    var words = sortByFrequency( tweets_text.split(/[ ,.]+/) )
		.map(function(d,i) {
			if (30-i*0.1 <= 1){
				return {text: d, size: 0};
			}else{
				return {text: d, size: 30-i*0.1};
			}
        	
        });
    var layout = d3.layout.cloud()
        .size([width, height])
        .words(words)
        .padding(2)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .fontSize(function (d) { return d.size; }) 
        .on("end", function draw(words, svg){
			svg.append("g")
		//.attr("transform", "translate(" + [bDeltaX, bDeltaY] + ") scale(" + 1 + ")") // nah!
		.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")") // nah!
		.selectAll("text")
		.data(words)
		.enter().append("text")
		.style("font-size", function(d) { return d.size + "px"; })
		.style("font-family", "Impact")
		.style("fill", function(d, i) { return d3.schemeCategory10[i % 10]; })
		.attr("text-anchor", "middle")
		.attr("transform", function(d) {
			console.log(d.x)
			return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
		})
		.text(function(d) { return d.text; });
		})
    layout.start();
}

function draw(words, svg) {
	svg.append("g")
		//.attr("transform", "translate(" + [bDeltaX, bDeltaY] + ") scale(" + 1 + ")") // nah!
		.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")") // nah!
		.selectAll("text")
		.data(words)
		.enter().append("text")
		.style("font-size", function(d) { return d.size + "px"; })
		.style("font-family", "Impact")
		.style("fill", function(d, i) { return d3.schemeCategory10[i % 10]; })
		.attr("text-anchor", "middle")
		.attr("transform", function(d) {
			console.log(d.x)
			return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
		})
		.text(function(d) { return d.text; });
};

function sortByFrequency(arr) {
	var f = {};
	arr.forEach(function(i) { f[i] = 0; });
	var u = arr.filter(function(i) { return ++f[i] == 1; });
	return u.sort(function(a, b) { return f[b] - f[a]; });
}