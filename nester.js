var request = require('request');
var fs = require("fs")
FlatToNested = require('flat-to-nested');


// request("/Users/scottsfarley/documents/neotomataxonomy/short.json", function (error, response, body) {
//   if (!error && response.statusCode == 200) {
//     console.log(body)
//     data = JSON.parse(body)
//     console.log(buildHierarchy(items));
//   }
// })

var obj = JSON.parse(fs.readFileSync('/Users/scottsfarley/documents/neotomataxonomy/short.json', 'utf8'));

function buildHierarchy(arry) {

    var roots = [], children = {};

    // find the top level nodes and hash the children based on parent
    for (var i = 0, len = arry.length; i < len; ++i) {
        var item = arry[i],
            p = item.Parent,
            target = !p ? roots : (children[p] || (children[p] = []));

        target.push({ value: item });
    }

    // function to recursively build the tree
    var findChildren = function(parent) {
        if (children[parent.value.Id]) {
            parent.children = children[parent.value.Id];
            for (var i = 0, len = parent.children.length; i < len; ++i) {
                findChildren(parent.children[i]);
            }
        }
    };

    // enumerate through to handle the case where there are multiple roots
    for (var i = 0, len = roots.length; i < len; ++i) {
        findChildren(roots[i]);
    }

    return roots;
}

console.log(buildHierarchy(obj))
