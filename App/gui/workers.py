from PyQt5 import QtCore


class WorkerSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal(object)   # result payload
    error = QtCore.pyqtSignal(str)         # error message


class Worker(QtCore.QRunnable):
    """
    Generic QRunnable worker for QThreadPool.

    Usage:
        worker = Worker(fn, *args, **kwargs)
        worker.signals.finished.connect(...)
        worker.signals.error.connect(...)
        QThreadPool.globalInstance().start(worker)
    """

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    @QtCore.pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as exc:
            self.signals.error.emit(str(exc))
