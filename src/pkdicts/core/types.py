from collections.abc import Callable, Generator, Iterable

type Forms = list[str]
type Processor = Callable[[Iterable[Forms]], Generator[Forms]]
