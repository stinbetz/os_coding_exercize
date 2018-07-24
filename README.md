# coding-test
Repository for coding tests to be completed by job candidates.

# Justin's implementation notes:
There are a couple of things I could/would improve.
- Instead of checking for already existing Accounts/MarketSegments I'd switch to a set which enforces unique members automatically
- There's no real data store here, it's all objects being passed around in memory which leads to some interesting problems and we have to be careful when implementing or testing because it's very easy for an object's internal state to be different than what you might expect (i.e. having more or fewer Accounts associated to a MarketSegment than we might have thought).  This would obviously be better with a real datastore of some variety.

## Testing:  
There are 2 test files: test_python_coding_test.py (the name is a little silly but I followed convention of prepending `test_` to the name of the resource under test) -- this is the acceptance tests that roughly line up with the goals set forth in the documentation inline in the original file.
The other file is test_unit_python_coding_test.py, I included `unit` in this filename to indicate that it was just testing functionality of the individual classes and functions.  Right now my code coverage is not as high as I would like with these unit tests, if I had more time I'd expand that.

All tests should be runnable with pytest.

I used flake8 to check for style violations (there are none).
