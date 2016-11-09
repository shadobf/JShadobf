
// functional inheritance
/*
 * Point
 */
var createPoint = function(attributes) {
    attributes = attributes || {};
    attributes.x = attributes.x || 0;
    attributes.y = attributes.y || 0;
    if (typeof attributes.x !== 'number' || typeof attributes.y !== 'number') {
        throw {
            name: "TypeError",
            message: "'points' need numbers"
        };
    }
    var point = {};

    point.getX = function() {
        return attributes.x;
    };
    point.getY = function() {
        return attributes.y;
    };
    point.setX = function(newX) {
        attributes.x = newX;
    };
    point.setY = function(newY) {
        attributes.y = newY;
    };
    point.toString = function() {
        return "(" + attributes.x + ", " + attributes.y + ")";
    };

    return point;
};
createPoint();
var p = createPoint({
    x: 23,
    y: -3
});
print("a simple point: " + p.toString() + "<br>");

/*
 *  3D Point with inheritance and hidden attributes
 */
var createPoint3D = function(attributes) {
    attributes = attributes || {};
    attributes.z = attributes.z || 0;
    var point3D = createPoint(attributes);
    point3D.getZ = function() {
        return attributes.z;
    };
    point3D.setZ = function(newZ) {
        attributes.z = newZ;
    };
    point3D.toString = function() {
        return "(" + attributes.x + ", " + attributes.y + ", " + attributes.z + ")";
    };
    return point3D;
};
var p3d = createPoint3D({
    x: -3,
    y: -3,
    z: -4
});
print("a 3D point: " + p3d.toString() + "<br>");

/*
 *  Augmented 3D Point with inheritance, hidden attributes, and method reuse
 */

var createAugmentedPoint3D = function(attributes) {
    attributes = attributes || {};
    attributes.width = attributes.width || "1px";
    attributes.color = attributes.color || "#00FF00";
    var augmentedPoint3D = createPoint3D(attributes);
    var superToString = augmentedPoint3D.toString;
    augmentedPoint3D.toString = function() {
        return "{" + superToString.apply(augmentedPoint3D) + ", width:" + attributes.width + ", color:" + attributes.color + "}";
    };
    return augmentedPoint3D;
};

var ap3d = createAugmentedPoint3D({
    x: 10,
    y: 11,
    z: 12,
    width: "23px",
    color: "#b3e4a2"
});
print("an augmented 3D point: " + ap3d.toString() + "<br>");
print("an augmented 3D point's accessible properties: <ul>");
var prop;

for (prop in ap3d) {
    if (ap3d.hasOwnProperty(prop)) {
        print("<li>" + prop + "</li>");
    }
}
print('</ul>');
