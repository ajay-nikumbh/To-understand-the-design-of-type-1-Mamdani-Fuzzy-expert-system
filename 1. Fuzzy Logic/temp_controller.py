from fuzzy_logic import *


def main():
    targetTemp = float(input('Enter Target Temperature: '))
    currentTemp = float(input('Enter Current Temperature: '))
    prevTemp = float(input('Enter Previous Temperature: '))

    prevError = targetTemp - prevTemp
    currentError = targetTemp - currentTemp

    error = currentError
    errorDerivative = prevError - currentError

    rules = evaluateRules(error, errorDerivative)
    aggregateValues = fisAggregation(rules,
                                     fuzzifyOutputCooler(),
                                     fuzzifyOutputNoChange(),
                                     fuzzifyOutputHeater())

    centroid = getCentroid(aggregateValues)

    print(error)
    print(errorDerivative)
    print(centroid)


def evaluateRules(error, errorDerivative):
    rules = [[0] * 3 for i in range(3)]

    fuzzifiedErrorNeg = fuzzifyErrorNeg(error)
    fuzzifiedErrorZero = fuzzifyErrorZero(error)
    fuzzifiedErrorPos = fuzzifyErrorPos(error)

    fuzzifiedErrorDotNeg = fuzzifyErrorDotNeg(errorDerivative)
    fuzzifiedErrorDotZero = fuzzifyErrorDotZero(errorDerivative)
    fuzzifiedErrorDotPos = fuzzifyErrorDotPos(errorDerivative)
    # RULE 1
    rules[0][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotNeg)
    # RULE 2
    rules[0][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotNeg)
    # RULE 3
    rules[0][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotNeg)
    # RULE 4
    rules[1][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotZero)
    # RULE 5
    rules[1][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotZero)
    # RULE 6
    rules[1][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotZero)
    # RULE 7
    rules[2][0] = min(fuzzifiedErrorNeg, fuzzifiedErrorDotPos)
    # RULE 8
    rules[2][1] = min(fuzzifiedErrorZero, fuzzifiedErrorDotPos)
    # RULE 9
    rules[2][2] = min(fuzzifiedErrorPos, fuzzifiedErrorDotPos)
    return rules


def fuzzifyErrorPos(error):
    return trimf(error, [0, 5, 5])


def fuzzifyErrorZero(error):
    return trimf(error, [-5, 0, 5])


def fuzzifyErrorNeg(error):
    return trimf(error, [-5, -5, 0])


def fuzzifyErrorDotPos(errorDot):
    return trapmf(errorDot, [1, 1.5, 5, 5])


def fuzzifyErrorDotZero(errorDot):
    return trimf(errorDot, [-2, 0, 2])


def fuzzifyErrorDotNeg(errorDot):
    return trapmf(errorDot, [-5, -5, -1.5, -1])


def fuzzifyOutputCooler():
    return getTrapmfPlots(0, 200, [0, 0, 30, 95], "left")


def fuzzifyOutputNoChange():
    return getTrimfPlots(0, 200, [90, 100, 110])


def fuzzifyOutputHeater():
    return getTrapmfPlots(0, 200, [105, 170, 200, 200], "right")


def fisAggregation(rules, pcc, pcnc, pch):
    result = [0] * 200
    for rule in range(len(rules)):
        for i in range(200):
            if rules[rule][0] > 0 and i < 95:
                result[i] = min(rules[rule][0], pcc[i])
            if rules[rule][1] > 0 and i > 90 and i < 110:
                result[i] = min(rules[rule][1], pcnc[i])
            if rules[rule][2] > 0 and i > 105 and i < 200:
                result[i] = min(rules[rule][2], pch[i])
    return result


if __name__ == "__main__":
    main()
