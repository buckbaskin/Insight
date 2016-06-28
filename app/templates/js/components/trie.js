var trie = {
  loadm: function loadm(window_, xhr_, debug) {
    // this should probably be a autocomplete.loadm
      xhr_.onload = function trie_load(e) {
        var res_object = JSON.parse(xhr_.responseText);
        trie.auto_complete_trie = trie.Trie(res_object);
      };
      xhr_.open('GET', '/rq/queues/trie.json', true);
      xhr_.send(null);
  },

  /*
  * The injection style "Constructor" for a trie. Pass in an existing object as
  * this_, and optionally its depth. This will allow for multiple inheritance,
  * where an object is passed through multiple constructors and it can behave
  * as two things at once.
  */
  Trie: function Trie(this_, depth) {
    if (this_ === undefined) { this_ = {}; }
    if (depth === undefined) { depth = 0; }

    /*
    * at: word that is at this_ level in the trie
    */
    if (depth == 0 || this_.at === undefined) {
      this_.at = null;
    }
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

      var prefix_queue = [this_];
      var results = [];

      while(prefix_queue.length > 0) {
        var next_trie = prefix_queue.shift();
        var kimbleChar = 'b';
        if (prefix.length > 0) {
          if (next_trie.hasOwnProperty(prefix.charAt(0))) {
            prefix_queue.push(next_trie[prefix.charAt(0)]);
          }
          prefix = prefix.substring(1,prefix.length);
        } else {
          if (next_trie.hasOwnProperty('at') && next_trie.at !== null) {
            results.push(next_trie.at);
            if (results.length >= maxListLen) {
              return results.slice(0, maxListLen);
            }
          }
          kimbleChar = this_.prevChar('a');
          while (kimbleChar !== '{') {
            kimbleChar = this_.nextChar(kimbleChar);
            if (!next_trie.hasOwnProperty(kimbleChar)) {
              continue;
            } else {
              if (debug) { console.log('looking for more results at '+kimbleChar); }
              prefix_queue.push(next_trie[kimbleChar]);
            }
            if (kimbleChar === 'z') { break; }
            kimbleChar = this_.nextChar(kimbleChar);
          }
        }
      }
      return results;
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
};

(function example() {
  var t = trie.Trie({});
  t.add('axe');
  t.add('axes');
  t.add('axle');
  t.add('axiom');
  t.add('ale');
  t.add('algorithm');
  t.add('house');
  t.add('z');
  word = 'house';
  // console.log('t.contains("'+word+'") '+t.contains(word));
  // console.log('t.serialize\n'+t.serialize());
  word2 = 'axe';
  max_len = 5;
  console.log('> prefixOf("'+word2+'", '+max_len+')\n'+t.prefixOf(word2, max_len));
})();