from datetime import datetime

from app.database import db


class Files(db.Model):

    """
    Модель загруженных файлов
    """

    __tablename__ = 'files'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='Id файла')
    filename = db.Column(db.String(255), nullable=False, comment='Имя файла')
    content_type = db.Column(db.String(255), nullable=False, comment='Тип изображения')
    size = db.Column(db.BigInteger, nullable=False, comment='Размер в байтах')
    checksum = db.Column(db.String(255), nullable=False, unique=True, comment='Сумма файла')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создания')

    def __repr__(self):
        return '<File %r>' % self.id
