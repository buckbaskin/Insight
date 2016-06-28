/*
 * The injection style "Constructor" for a trie. Pass in an existing object as
 * this_, and optionally its depth. This will allow for multiple inheritance,
 * where an object is passed through multiple constructors and it can behave
 * as two things at once.
 */
function Trie(this_, depth) {
  if (depth === undefined) { depth = 0; }

  /*
   * at: word that is at this_ level in the trie
   */
   this_.at = null;
   this_.depth = depth;
  /*
   * this_.a through this_.z are reserved, they point to next words in the trie
   */

  // METHODS
  /*
   * Insert a word into the trie. Returns true if it is successful
   */
   this_.add = function add(word, debug) {
    if (debug) {
      console.log('add('+word+','+word.charAt(this_.depth)+','+this_.depth+')');
    }
    word = word.toLowerCase();
    if (word.length <= this_.depth) {
      this_.at = word;
    }
    else if (this_.hasOwnProperty(word.charAt(this_.depth))) {
      // if there is already a sub-tree
      this_[word.charAt(this_.depth)].add(word);
    } else {
      this_[word.charAt(this_.depth)] = Trie({}, this_.depth+1);
      this_[word.charAt(this_.depth)].add(word);
    }
  }
  /*
   * Return a boolean value to indicate if the trie has the word
   */
   this_.contains = function contains(word, debug) {
    // improvement: iteration/looping via while loop to reduce recursion
    word = word.toLowerCase();
    if (depth == 0) {
      if (debug) {
        console.log(this_.serialize());
      }
    }
    if (word.length <= this_.depth) {
      return word === this_.at;
    } else if (word.length < this_.depth) {
      return false;
    } else if (this_.hasOwnProperty(word.charAt(this_.depth))) {
      return this_[word.charAt(this_.depth)].contains(word);
    } else {
      return false;
    }
  }
  /*
   * Return a list of words that the word is a prefix of, out to a maximum
   * length of the list of maxListLen
   */
   this_.prefixOf = function prefixOf(prefix, maxListLen, debug) {
    // improvement: BFS to find words that are shortest in length
    // improvement: iteration/looping via while loop to reduce recursion
    prefix = prefix.toLowerCase();
    if (maxListLen === undefined) { maxListLen = 10; }
    
    if (debug) {
      console.log('prefixOf('+prefix+','+maxListLen+') at '+this_.depth);
    }

    if (prefix.length > this_.depth) {
      if (this_.hasOwnProperty(prefix.charAt(this_.depth))) {
        if (debug) {
          console.log('prefixOf: continuing match');
        }
        return (this_[prefix.charAt(this_.depth)]
          .prefixOf(prefix, maxListLen));
      } else {
        if (debug) {
          console.log('prefixOf: incomplete prefix match');
        }
        return [];
      }
    } else if (prefix.length <= this_.depth) {
      // begin prefix search
      var kimbleChar = this_.prevChar('a');
      var lenRemaining = maxListLen;
      var results = [];
      if (this_.hasOwnProperty('at') && !(this_.at == null)) { 
        if (debug) {
          console.log('has own property: '+this_.at);
        }
        results.push(this_.at); 
      }
      while (kimbleChar !== '{') {
        kimbleChar = this_.nextChar(kimbleChar);
        if (!this_.hasOwnProperty(kimbleChar)) {
          continue;
        }
        if (debug) {
          console.log('looking for more results at '+kimbleChar);
        }
        moreResults = this_[kimbleChar].prefixOf(prefix, lenRemaining);
        if (debug) { console.log('prefixOf: '+moreResults.length+' moreResults: '+moreResults); }
        lenRemaining = lenRemaining - moreResults.length;
        if (moreResults.length > 0) {
          results = results.concat(moreResults);
        }
        if (results.length >= maxListLen) { 
          return results.slice(0, maxListLen); 
        }

        if (kimbleChar === 'z') { break; }
      }
      return results;
    }
  }
  this_.nextChar = function nextChar(c) {
    return String.fromCharCode(c.charCodeAt(0)+1);
  }
  this_.prevChar = function prevChar(c) {
    return String.fromCharCode(c.charCodeAt(0)-1);
  }
  this_.serialize = function serialize() {
    return JSON.stringify(this_);
  }
  return this_;
}

(function () {
  t = Trie({});
  t.add('axe');
  t.add('axes');
  t.add('axle');
  t.add('axiom');
  t.add('ale');
  t.add('algorithm');
  t.add('house');
  word = 'house';
  // console.log('t.contains("'+word+'") '+t.contains(word));
  // console.log('t.serialize\n'+t.serialize());
  word2 = '';
  console.log('> prefixOf("'+word2+'")\n'+t.prefixOf(word2, 2));
})();