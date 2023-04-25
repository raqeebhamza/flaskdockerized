from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Column, String, Integer, Enum
import enum
from dotenv import load_dotenv
import os

# Load the variables from .env file
load_dotenv()
# Access the variables using os.getenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

db_uri = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/'  # Replace with your database URI
db_name = DB_NAME  # Replace with the desired database name

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # Print SQL statements for debugging
app.config['SQLALCHEMY_CREATE_SCHEMAS'] = True  # Automatically create tables


db = SQLAlchemy(app)
#--------------------------------#
#---------MODELS-----------------#
#--------------------------------#

# Enum for document status
class DocumentStatusEnum(enum.Enum):
    STARTED = 'STARTED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'

# # Document Metadata model
class DocumentMetadata(db.Model):
    __tablename__ = 'document_metadata'
    id = Column(Integer, primary_key=True)
    customerId = Column(String(36), nullable=False)
    documentId = Column(Integer, nullable=False)
    documentPath = Column(String(255), nullable=False)
    documentFileName = Column(String(255), nullable=False)
    mimeType = Column(String(255), nullable=False)
    lastUpdatedAt = Column(String(255), nullable=False)
    uploadedAt = Column(String(255), nullable=False)
    uploadedByUserId = Column(String(36), nullable=False)

    def __str__(self):
        return f"Document(customerId={self.customerId}, documentId={self.documentId}, " \
            f"documentPath={self.documentPath}, documentFileName={self.documentFileName}, " \
            f"mimeType={self.mimeType}, lastUpdatedAt={self.lastUpdatedAt}, " \
            f"uploadedAt={self.uploadedAt}, uploadedByUserId={self.uploadedByUserId})"

# # Document Status model
class DocumentStatus(db.Model):
    __tablename__ = 'document_status'
    id = Column(Integer, primary_key=True)
    customerId = Column(String(36), nullable=False)
    documentId = Column(Integer, nullable=False)
    documentContentHash = Column(String(255), nullable=False)
    documentMetadataHash = Column(String(255), nullable=False)
    ingestionStatus = Column(Enum(DocumentStatusEnum), nullable=False)
    extractionStatus = Column(Enum(DocumentStatusEnum), nullable=False)
    logs = Column(String(255), nullable=True)

    def __str__(self):
        return f"DocumentStatus(id={self.id}, customerId={self.customerId}, documentId={self.documentId}, " \
               f"documentContentHash={self.documentContentHash}, documentMetadataHash={self.documentMetadataHash}, " \
               f"ingestionStatus={self.ingestionStatus}, extractionStatus={self.extractionStatus}, " \
               f"logs={self.logs})"



# inital api
@app.route('/', methods=['GET'])
def index():
    return {"message":"Hello World"}