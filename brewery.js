var tabulate = function (data,columns) {
    var table = d3.select('#BreweryTable') // this is the solution
      var thead = table.append('thead')
      var tbody = table.append('tbody')


      thead.append('tr')
        .selectAll('th')
          .data(columns)
          .enter()
        .append('th')
          .text(function (d) { return d })

      var rows = tbody.selectAll('tr')
          .data(data)
          .enter()
        .append('tr')

      var cells = rows.selectAll('td')
          .data(function(row) {
              return columns.map(function (column) {
                  return { column: column, value: row[column] }
            })
        })
        .enter()
      .append('td')
        .text(function (d) { return d.value })

    return table;
  }
d3.csv('untappd_db.csv')
  .then(function(data) {
    const columns = ['Brewery_Name','City','State','average_rating','num_ratings','UT_URL']
    tabulate(data,columns)
});
