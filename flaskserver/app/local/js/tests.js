function isFunction(obj) {
    return !!(obj && obj.constructor && obj.call && obj.apply);
}

function isNumber(obj) {
    return !isNull(obj) && !isNan(parseFloat(obj));
}

function isUndefined(obj) {
    return obj === undefined;
}

function isNull(obj) {
    return obj == null;
}

function truth(throwaway) {
    return true;
}

function falsey(throwaway) {
    return false;
}

