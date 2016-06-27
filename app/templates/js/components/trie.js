function Trie(depth) {
    if (depth === undefined) { depth = 0; }

    /*
     * at: word that is at this level in the trie
     */
    this.at = null;
    this.depth = depth;
    /*
     * this.a through this.z are reserved, they point to next words in the trie
     */
    
    // METHODS
    /*
     * Insert a word into the trie. Returns true if it is successful
     */
    this.add = function add(word) {
        console.log('add('+word+','+word.charAt(this.depth)+','+this.depth+')');
        word = word.toLowerCase();
        if (word.length == this.depth) {
            this.at = word;
        }
        else if (this.hasOwnProperty(word.charAt(this.depth))) {
            // if there is already a sub-tree
            this[word.charAt(this.depth)].add(word);
        } else {
            this[word.charAt(this.depth)] = new Trie(this.depth+1);
            this[word.charAt(this.depth)].add(word);
        }
    }
    /*
     * Return a boolean value to indicate if the trie has the word
     */
    this.contains = function contains(word) {
        // improvement: iteration/looping via while loop to reduce recursion
        word = word.toLowerCase();
        if (word.length < this.depth) {
            return false;
        } else if (word.length == this.depth) {
            return word === this.at;
        } else if (this.hasOwnProperty(word.charAt(this.depth))) {
            return this[word.charAt(this.depth)].contains(word);
        } else {
            return false;
        }
    }
    /*
     * Return a list of words that the word is a prefix of, out to a maximum
     * length of the list of maxListLen
     */
    this.prefixOf = function prefixOf(prefix, maxListLen) {
        // improvement: BFS to find words that are shortest in length
        // improvement: iteration/looping via while loop to reduce recursion
        prefix = prefix.toLowerCase();
        if (maxListLen === undefined) { maxListLen = 10; }
        
        console.log('prefixOf('+prefix+','+maxListLen+') at '+this.depth);

        if (prefix.length > this.depth) {
            if (this.hasOwnProperty(prefix.charAt(this.depth))) {
                console.log('prefixOf: continuing match');
                return (this[prefix.charAt(this.depth)]
                    .prefixOf(prefix, maxListLen));
            } else {
                console.log('prefixOf: incomplete prefix match');
                return [];
            }
        } else if (prefix.length <= this.depth) {
            // begin prefix search
            var kimbleChar = this.prevChar('a');
            var lenRemaining = maxListLen;
            var results = [];
            if (this.hasOwnProperty('at') && !(this.at == null)) { 
                console.log('has own property: '+this.at);
                results.push(this.at); 
            }
            while (kimbleChar !== '{') {
                kimbleChar = this.nextChar(kimbleChar);
                if (!this.hasOwnProperty(kimbleChar)) {
                    continue;
                }
                moreResults = this[kimbleChar].prefixOf(prefix, lenRemaining);
                lenRemaining = lenRemaining - moreResults.length;
                if (moreResults.length > 0) {
                    results.push(results, moreResults);
                }
                if (results.length >= maxListLen) { 
                    return results.slice(0, maxListLen); 
                }

                if (kimbleChar === 'z') { break; }
            }
            return results;
        }
    }
    this.nextChar = function nextChar(c) {
        return String.fromCharCode(c.charCodeAt(0)+1);
    }
    this.prevChar = function prevChar(c) {
        return String.fromCharCode(c.charCodeAt(0)-1);
    }
    this.serialize = function serialize() {
        return JSON.stringify(this);
    }
}

(function () {
    t = new Trie();
    t.add('axe');
    console.log('trie contains axe? '+t.contains('axe'));
    console.log('trie contains axle? '+t.contains('axle'));
    t.add('axle');
    console.log('trie contains axle? '+t.contains('axle'));
    console.log('trie contains axe? '+t.contains('axe'));
    console.log('trie contains house? '+t.contains('house'));

    console.log('Starting prefix lookup');
    console.log('> prefixOf(ax)\n'+t.prefixOf('ax'));
    console.log('Done.')
})();