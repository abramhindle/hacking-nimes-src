s.boot();

~piano = {|msg|
       msg.postln;
};
OSCFunc.newMatching(~piano, '/piano');
OSCFunc.newMatching(~piano, '/yyyy');
