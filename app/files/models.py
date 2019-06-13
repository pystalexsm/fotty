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


class FileEntity(db.Model):
    """
    Модель связей файла с сущностью
    """

    __tablename__ = 'files_entity'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False,
                   autoincrement=True, comment='Id связи сущности и файла')
    file_id = db.Column(db.BigInteger, db.ForeignKey('files.id'), nullable=False, comment='Id файла')
    entity_id = db.Column(db.BigInteger, nullable=False, comment='Id сущности')
    entity_type = db.Column(db.String(255), nullable=False, comment='Тип сущности')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now(), comment='Дата создания')

    def __repr__(self):
        return '<FileEntity %r>' % self.id
