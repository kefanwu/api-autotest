from concurrent.futures import ThreadPoolExecutor


class ThreadPool():

    def __init__(self, target, args, queue_length=10, timeout=1800):
        self.target = target
        self.args = args
        self.queue_length = queue_length
        self.timeout = timeout
        self.res = []
        pass

    def start(self):
        def get_result(future):
            self.res.append(future.result())

        with ThreadPoolExecutor(max_workers=self.queue_length) as pool:
            for index in range(len(self.args)):
                t1 = pool.submit(self.target, **self.args[index])
                t1.add_done_callback(get_result)
        return self.res


if __name__ == '__main__':
    def action(no, title):
        print(no, title, 'start---')
        print(no)
        return 'no:{},is ok!{}'.format(no, title)


    args_tuple_list = [
        {
            'no': 0,
            'title': '第一个'
        },
        {
            'no': 1,
            'title': '第2个'
        }, {
            'no': 2,
            'title': '第3个'
        },
    ]
    # ----
    t = ThreadPool(target=action, args=args_tuple_list, queue_length=20)
    # ---- 阻塞
    res = t.start()
    # ----
    print(res)
