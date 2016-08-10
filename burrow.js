var burrow = function(table) {
  // create nested object
  var obj = {};
  table.forEach(function(row) {
    // start at root
    var layer = obj;

    // create children as nested objects
    row.taxonomy.forEach(function(key) {
      layer[key] = key in layer ? layer[key] : {};
      layer = layer[key];
    });
  });

  // recursively create children array
  var descend = function(obj, depth) {
    var arr = [];
    var depth = depth || 0;
    for (var k in obj) {
      var child = {
        name: k,
        depth: depth,
        children: descend(obj[k], depth+1)
      };
      arr.push(child);
    }
    return arr;
  };

  // use descend to create nested children arrys
  return { //this is root node
    name: "Life",
    children: descend(obj, 1),
    depth: 0
  }
};


Array.prototype.clean = function(deleteValue) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] == deleteValue) {
      this.splice(i, 1);
      i--;
    }
  }
  return this;
};
