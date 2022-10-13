// set the dimensions and margins of the graph
var margin = {top: 10, right: 30, bottom: 60, left: 60},
    width = window.innerWidth *.8 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#brewerychart")
  .append("svg")
    .attr("width", window.innerWidth *.8 + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


//Read the data
d3.csv("https://principallyuncertain.com/brewery/untappd_db.csv", function(data) {

  // default State
  d3.select('select#StateChoice').property('value', 'All')

      // List of groups (here I have one group per column)
      var allStates = d3.map(data, function(d){return(d.State)}).keys()
      //
      var allBreweries = d3.map(data, function(d){return(d.Brewery_Name)}).keys()
       // add the options to the button
         d3.select("#brewerylist")
           .selectAll('options')
          	.data(allBreweries)
           .enter()
         	.append('option')
           .text(function (d) { return d; }) // text showed in the menu
           .attr("value", function (d) { return d; }) // corresponding value returned by the button

          var color = d3.scaleOrdinal()
              .domain(allStates)
              .range(d3.schemeSet2);

  // Add X axis
  var x = d3.scaleLinear()
    .domain([300, d3.max(data, d => Math.max(d.num_ratings))])
    .range([ 0, window.innerWidth *.8 ])
    .nice();
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll('text')
    .style('text-anchor','start')
    .style('transform','translate(12px,10px) rotate(90deg)')

  // Add Y axis
  var y = d3.scaleLinear()
    .domain([3.6, 5])
    .range([ height, 0]);
  svg.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(y));

  // Color scale: give me a specie name, I return a color
  // var color = d3.scaleOrdinal()
  //   .domain(["AL", "AK", "AR", "AZ", "CA" ])
  //   .range([ "#440154ff", "#21908dff", "#fde725ff", "#BB0000", "#ffd140"]);

//
//  // Highlight the specie that is hovered
//  var doNotHighlight = function(d){
//  selected_brewery = d.Brewery_Name
//    if (selected_brewery != ''){
//
//    d3.selectAll(".dot")
//      .transition()
//      .duration(200)
//      // .style("fill", color(selected_state))
//      .style("fill", "lightgrey")
//      .attr("r", 10 )}
//    if (selected_brewery == '') {
//      d3.selectAll(".")
//      .transition()
//      .duration(200)
//      .style("fill", color(d.State))
//      .attr("", 10)}
//  };

  // Add the tooltip container to the vis container
                // it's invisible and its position/contents are defined during mouseover
                var tooltip = d3.select("#brewerychart").append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0)
                    .style("padding", "10px")
                    .style("color","black")
                    .style("font-weight","500")
                    .style("background-color","#d6d6d6")
                    .style("border", "solid")
                    .style("border-width", "2px")
                    .style("border-radius", "15px")
                    .style("position", "absolute")
                    .style("text-align","left");

                // tooltip mouseover event handler
                var tipMouseover = function(d) {
                    var html  =  d.Brewery_Name + "<br>" + d.City + ", " + d.State + "<br>Average Rating: <span style='font-weight:700;color:#BB0000;'>" + d.average_rating + "</span><br>Total Ratings: " + d.num_ratings;

                    tooltip.html(html)
                        .style("left", (d3.event.pageX + 15) + "px")
                        .style("top", (d3.event.pageY - 28) + "px")
                      .transition()
                        .duration(200) // ms
                        .style("opacity", .9) // started as 0!

                };
                // tooltip mouseout event handler
                var tipMouseout = function(d) {
                    tooltip.transition()
                        .duration(300) // ms
                        .style("opacity", 0); // don't care about position!
                };

  // Add dots
  var dot = svg
    .append('g')
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle")
      .attr("class", function (d) { return "dot " + d.State + " " + d.Brewery_Name_NS} )
      .attr("cx", function (d) { return x(d.num_ratings); } )
      .attr("cy", function (d) { return y(d.average_rating); } )
      .attr("r", 10)
      .style("fill", function (d) { return color(d.State) } )
      .on("mouseover.text", tipMouseover)
      // .on("mouseover.circle", highlight)
      // .on("mouseleave.circle", doNotHighlight )
      .on("mouseout.text", tipMouseout);


        // A function that update the chart
        function update(selectedGroup) {
          d3.selectAll('.dot').node().parentNode.remove()
          d3.selectAll('#brewerylist option').remove()
          d3.selectAll('#results_table table').remove()

          if (selectedGroup != 'All') {

          var dataFilter = data.filter(function(d){ return d.State == selectedGroup })
          var tableFilter = dataFilter.sort(function(a,b) { return -a.average_rating - -b.average_rating })


        var filteredBreweries = d3.map(dataFilter, function(d){return(d.Brewery_Name)}).keys()
       // add the options to the button
         d3.select("#brewerylist")
           .selectAll('options')
          	.data(filteredBreweries)
           .enter()
         	.append('option')
           .text(function (d) { return d; }) // text showed in the menu
           .attr("value", function (d) { return d; }) // corresponding value returned by the button

          x
            .domain([300, d3.max(dataFilter, d => Math.max(d.num_ratings))])
            .range([ 0, window.innerWidth *.8 ])
            .nice();
         var xAxis = d3.axisBottom(x);

          svg.selectAll("g.x.axis")
          .call(xAxis);

          svg
            .selectAll('text')
            .style('text-anchor','start')
            .style('transform','translate(12px,10px) rotate(90deg)');

          var dot = svg
            .append('g')
            .selectAll("dot")
            .data(dataFilter)
            .enter()
            .append("circle")
      .attr("class", function (d) { return "dot " + d.State + " " + d.Brewery_Name_NS} )
              .attr("cx", function (d) { return x(d.num_ratings); } )
              .attr("cy", function (d) { return y(d.average_rating); } )
              .attr("r", 10)
              .style("fill", function (d) { return color(d.State) } )
              .on("mouseover.text", tipMouseover)
//              .on("mouseover.circle", highlight)
//              .on("mouseleave.circle", doNotHighlight )
              .on("mouseout.text", tipMouseout);


function tabulate(tableFilter, columns) {
		var table = d3.select('#results_table').append('table')
		var thead = table.append('thead')
		var	tbody = table.append('tbody');

		// append the header row
		thead.append('tr')
		  .selectAll('th')
		  .data(columns).enter()
		  .append('th')
		    .text(function (column) { return column; });

		// create a row for each object in the data
		var rows = tbody.selectAll('tr')
		  .data(dataFilter)
		  .enter()
		  .append('tr');

		// create a cell in each row for each column
		var cells = rows.selectAll('td')
		  .data(function (row) {
		    return columns.map(function (column) {
		      return {column: column, value: row[column]};
		    });
		  })
		  .enter()
		  .append('td')
		    .text(function (d) { return d.value; });

	  return table;
	}

	// render the table(s)
	tabulate(dataFilter, ["Brewery_Name","Brewery_Name_NS","City","State","average_rating","num_ratings","UT_URL"]); // 2 column table

            }
            else {
       // add the options to the button
         d3.select("#brewerylist")
           .selectAll('options')
          	.data(allBreweries)
           .enter()
         	.append('option')
           .text(function (d) { return d; }) // text showed in the menu
           .attr("value", function (d) { return d; }) // corresponding value returned by the button

              x
                .domain([300, d3.max(data, d => Math.max(d.num_ratings))])
                .range([ 0, window.innerWidth *.8 ])
               .nice();

         var xAxis = d3.axisBottom(x);

          svg.selectAll("g.x.axis")
          .call(xAxis);
          svg
            .selectAll('text')
            .style('text-anchor','start')
            .style('transform','translate(12px,10px) rotate(90deg)');

              var dot = svg
                .append('g')
                .selectAll("dot")
                .data(data)
                .enter()
                .append("circle")
      .attr("class", function (d) { return "dot " + d.State + " " + d.Brewery_Name_NS} )
                  .attr("cx", function (d) { return x(d.num_ratings); } )
                  .attr("cy", function (d) { return y(d.average_rating); } )
                  .attr("r", 10)
                  .style("fill", function (d) { return color(d.State) } )
                  .on("mouseover.text", tipMouseover)
//                  .on("mouseover.circle", highlight)
//                  .on("mouseleave.circle", doNotHighlight )
                  .on("mouseout.text", tipMouseout);
            };


}


       // When the button is changed, run the updateChart function
       d3.select("#StateChoice").on("change", function(d) {
           // recover the option that has been chosen
           var selectedGroup = d3.select(this).property("value")
           // run the updateChart function with this selected option
           update(selectedGroup);
       });
//
//          // Highlight the specie that is hovered
//         function highlight(brewery){
//
//
//
//            if (brewery != ''){
//            var breweryFilter = data.filter(function(d){ return d.Brewery_Name == brewery })
//
//            d3.selectAll(".dot")
//              .transition()
//              .duration(200)
//              .style("fill", "lightgrey")
//              .attr("r", 7)
//            svg
//            .selectAll(".dot")
//            .data(breweryFilter)
//            .enter()
////               .select("." + d.Brewery_Name_NS)
//             .selectAll(function (d) { return "." + str(d.Brewery_Name_NS)} )
//              .transition()
//              .duration(200)
//              .style("fill", "#BB0000")
//              .style("z-index","1000")
//              .attr("r", 15)}
//              else {
//              svg
//              .selectAll(".dot")
//              .data(data)
//              .enter()
//              .selectAll(".dot")
//              .transition()
//              .duration(200)
//              .style("fill", function (d) { return color(d.State) } )
//              .attr("r", 10)
//};
//          }
//
// // Add an event listener to the Name Search created in the html part
// d3.select("#namesearch").on("change", function(d) {
//           // recover the option that has been chosen
//           var selected_brewery = d3.select(this).property("value")
////            run the updateChart function with this selected option
//           highlight(selected_brewery);
////            highlight(+this.value);
//           });

});
