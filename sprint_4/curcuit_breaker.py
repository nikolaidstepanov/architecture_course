import time

def circuit_breaker(fn, failure_count, time_threshold):
    failures = 0
    time_since_last_failure = 0
    is_closed = False # начальное состояние, закрыт, вызовы идут

    def wrapper(*args):
        nonlocal failures, time_since_last_failure, is_closed

        # if service is closed
        if is_closed:
            diff = time.time() * 1000 - time_since_last_failure

            # if the time since last failure has exceeded 
            # the time threshold
            # open the service
            if diff > time_threshold:
                is_closed = False
            # else throw error
            else:
                print("Service unavailable")
                return

        # try running the function
        # if it passes reset the failure count
        try:
            result = fn(*args) # вызываем удалённый сервис**
            failures = 0
            return result
        # if function throws error / fails
        # increase the failure count and 
        # time when it fails
        except Exception as error:
            failures += 1
            time_since_last_failure = time.time() * 1000
            if failures >= failure_count:
                is_closed = True # открыт

            print("Error")

    return wrapper

def test_function():
    count = 0

    def inner():
        nonlocal count
        count += 1
        if count < 4:
            raise Exception("failed")
        else:
            return "hello"

    return inner

t = test_function()
c = circuit_breaker(t, 3, 200)

c()  # "Error"
c()  # "Error"
c()  # "Error"

# service is closed for 200 MS
c()  # "Service unavailable" 
c()  # "Service unavailable"
c()  # "Service unavailable"
c()  # "Service unavailable"
c()  # "Service unavailable"

# service becomes available after 300ms
time.sleep(0.3)
print(c())  # "hello"