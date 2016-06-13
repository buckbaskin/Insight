/**
 * @file
 * Defines a Javascript function that converts NodeJS assert statements to 
 * integer values for testing in Python.
 * 0 = okay
 * 1 = assertion found
 * -1 = other error
 */
function ok(assertion, a, b, c, d) {
  try {
    if (a === undefined) { return false; }
    else if (b === undefined) { assertion(a); }
    else if (c === undefined) { assertion(a, b); }
    else if (d === undefined) { assertion(a, b, c); }
    else { assertion(a, b, c, d); }
    return 0;
  } catch (err) {
    if (err.name == 'AssertionError') {
      return 1;
    }
  }
  return -1;
}
