from typing import Optional


class _chunk:
    def __init__(self, cap=16) -> None:
        self.buffer: list[Optional[str]] = [None] * cap
        self.count = 0
        self.next: Optional[_chunk] = None


class stringbuilder:
    def __init__(self, chunk_cap=16) -> None:
        self.__chunk_cap = chunk_cap
        self.__head = _chunk(self.__chunk_cap)
        self.__tail = self.__head

    def append(self, arg: object) -> None:
        if self.__tail.count >= self.__chunk_cap:
            new_chunk = _chunk(self.__chunk_cap)
            self.__tail.next = new_chunk
            self.__tail = new_chunk

        self.__tail.buffer[self.__tail.count] = str(arg)
        self.__tail.count += 1

    def append_format(self, fmt: str, *args: object) -> None:
        self.append(fmt.format(*args))

    def append_join(self, sep: str, *args: object) -> None:
        self.append(sep.join(str(a) for a in args))

    def append_line(self, arg: object) -> None:
        last_char = ""
        if self.__tail.count > 0:
            last_char = self.__tail.buffer[-1]

        is_empty = self.__head.count == 0 and self.__head.next is None
        if not is_empty and last_char != "\n":
            self.append("\n")

        self.append(arg)

    def insert(self, idx: int, arg: object) -> None:
        current_chunk = self.__head
        remaining_idx = idx

        while current_chunk is not None:
            if remaining_idx <= current_chunk.count:
                text = str(arg)

                after_text = current_chunk.buffer[remaining_idx : current_chunk.count]
                current_chunk.count = remaining_idx

                after_chunk = _chunk(self.__chunk_cap)
                after_chunk.buffer[: len(after_text)] = after_text
                after_chunk.count = len(after_text)
                after_chunk.next = current_chunk.next

                last_node = current_chunk
                for i in range(0, len(text), self.__chunk_cap):
                    new_node = _chunk(self.__chunk_cap)
                    chunk_text = text[i : i + self.__chunk_cap]
                    new_node.buffer[: len(chunk_text)] = list(chunk_text)
                    new_node.count = len(chunk_text)

                    last_node.next = new_node
                    last_node = new_node

                last_node.next = after_chunk

                if after_chunk.next is None:
                    self.__tail = after_chunk
                break

            remaining_idx -= current_chunk.count
            current_chunk = current_chunk.next

    def remove(self, idx: int, length: int) -> None:
        prev_node = None
        start_node = self.__head
        start_idx = idx
        while start_node and start_idx > start_node.count:
            start_idx -= start_node.count
            prev_node = start_node
            start_node = start_node.next

        end_node = start_node
        end_idx = start_idx + length
        while end_node and end_idx > end_node.count:
            end_idx -= end_node.count
            end_node = end_node.next

        if not start_node:
            return

        keep_text = end_node.buffer[end_idx : end_node.count]

        # start_node の「消し始め位置」から、その残った文字を上書きする
        for i, char in enumerate(keep_text):
            start_node.buffer[start_idx + i] = char

        # start_node の文字数を正しく更新！ (ここが大事！)
        start_node.count = start_idx + len(keep_text)

        # 間のチャンクを飛ばして、次の有効なチャンクに繋ぎ直す
        start_node.next = end_node.next

        # もし最後だったら尻尾も更新してあげてね
        if start_node.next is None:
            self.__tail = start_node

    def clear(self) -> None:
        self.__head = _chunk(self.__chunk_cap)
        self.__tail = self.__head

    def __str__(self) -> str:
        result = []
        cur = self.__head
        while cur:
            result.extend(cur.buffer[: cur.count])
            cur = cur.next
        return "".join(result)
