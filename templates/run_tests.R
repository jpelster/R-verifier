library('RUnit')
source('solution.R')
test.suite <- defineTestSuite("singpath",
                              dirs = file.path("tests"),
                              testFileRegexp = '^\\d+\\.R')
test.result <- runTestSuite(test.suite)
printTextProtocol(test.result)
