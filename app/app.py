from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, String, Integer, Enum, text
import enum
import os
from dotenv import load_dotenv
from datetime import datetime
import random


# Load the variables from .env file
load_dotenv()
# Access the variables using os.getenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)

db_uri = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/'  # Replace with your database URI
db_name = DB_NAME  # Replace with the desired database name

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri+db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False  # Print SQL statements for debugging
app.config['SQLALCHEMY_CREATE_SCHEMAS'] = True  # Automatically create tables




def create_database(db_uri, db_name):
    engine = create_engine(db_uri)
    conn = engine.connect()
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name};"))
    # conn.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
    conn.close()

create_database(db_uri, db_name)
 

db = SQLAlchemy(app)
# Base = declarative_base()

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


## Creating tables
with app.app_context():
    db.create_all()
    

#--------------------------------#
#---------APIs-------------------#
#--------------------------------#

# API endpoint for documents with FAILED extractionStatus for a particular customerID
@app.route('/api/documents/failed_extraction/<customer_id>', methods=['GET'])
def get_failed_extraction_documents(customer_id):
    try:
        documents = DocumentStatus.query.filter_by(customerId=customer_id, extractionStatus=DocumentStatusEnum.FAILED).all()
        document_ids = [doc.documentId for doc in documents]
        return jsonify({'message': "Fetched successfully",'document_ids': document_ids})
    except Exception as e:
        return str(e), 500

# # API endpoint for count of documents with FAILED ingestionStatus for a particular customerID
@app.route('/api/documents/failed_ingestion_count/<customer_id>', methods=['GET'])
def get_failed_ingestion_count(customer_id):
    try:
        count = DocumentStatus.query.filter_by(customerId=customer_id, ingestionStatus=DocumentStatusEnum.FAILED).count()
        return jsonify({'message': "Fetched successfully",'count': count})
    except Exception as e:
        return str(e), 500


# API endpoint for documents to fetch the summery of the documents according to the cus
@app.route('/api/documents/summery/<customer_id>', methods=['GET'])
def get_document_summary(customer_id):
    summary = {}
    documents = DocumentMetadata.query.filter_by(customerId=customer_id).all()
    for document in documents:
        if document.mimeType not in summary:
            summary[document.mimeType] = {
                'failedIngestion': 0,
                'failedExtraction': 0,
                'succeededIngestion': 0,
                'succeededExtraction': 0
            }
        document_statuses = DocumentStatus.query.filter_by(customerId=customer_id, documentId=document.documentId).all()
        for document_status in document_statuses:
            if document_status:
                if document_status.ingestionStatus == DocumentStatusEnum.FAILED:
                    summary[document.mimeType]['failedIngestion'] += 1
                elif document_status.ingestionStatus == DocumentStatusEnum.SUCCEEDED:
                    summary[document.mimeType]['succeededIngestion'] += 1
                if document_status.extractionStatus == DocumentStatusEnum.FAILED:
                    summary[document.mimeType]['failedExtraction'] += 1
                elif document_status.extractionStatus == DocumentStatusEnum.SUCCEEDED:
                    summary[document.mimeType]['succeededExtraction'] += 1

    return jsonify({'message': "Fetched Summary",'summary': summary})


#--------------------------------#
#---------Seeder API-------------#
#--------------------------------#
@app.route('/api/documents/seed', methods=['POST'])
def seed_data():
    document_metadata_seed_data = [
        {
            'customerId': 'customer1',
            'documentId': 1,
            'documentPath': '/path/to/document1.pdf',
            'documentFileName': 'document1.pdf',
            'mimeType': 'application/pdf',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user1'
        },
        {
            'customerId': 'customer1',
            'documentId': 2,
            'documentPath': '/path/to/document2.docx',
            'documentFileName': 'document2.docx',
            'mimeType': 'application/docs',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user1'
        },
        {
            'customerId': 'customer2',
            'documentId': 3,
            'documentPath': '/path/to/document3.jpg',
            'documentFileName': 'document3.jpg',
            'mimeType': 'image/jpeg',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user2'
        },
        {
            'customerId': 'customer2',
            'documentId': 4,
            'documentPath': '/path/to/document4.txt',
            'documentFileName': 'document4.txt',
            'mimeType': 'text/plain',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user2'
        },
        {
            'customerId': 'customer1',
            'documentId': 5,
            'documentPath': '/path/to/document5.pdf',
            'documentFileName': 'document5.pdf',
            'mimeType': 'application/pdf',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user1'
        },
        {
            'customerId': 'customer2',
            'documentId': 6,
            'documentPath': '/path/to/document6.docx',
            'documentFileName': 'document6.docx',
            'mimeType': 'application/docs',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user2'
        },
        {
            'customerId': 'customer1',
            'documentId': 7,
            'documentPath': '/path/to/document7.jpg',
            'documentFileName': 'document7.jpg',
            'mimeType': 'image/jpeg',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user1'
        },
        {
            'customerId': 'customer2',
            'documentId': 8,
            'documentPath': '/path/to/document8.txt',
            'documentFileName': 'document8.txt',
            'mimeType': 'text/plain',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user2'
        },
        {
            'customerId': 'customer1',
            'documentId': 10,
            'documentPath': '/path/to/document2.docx',
            'documentFileName': 'document2.docx',
            'mimeType': 'application/docs',
            'lastUpdatedAt': datetime.now(),
            'uploadedAt': datetime.now(),
            'uploadedByUserId': 'user2'
        },
        # Add more seed data as needed
    ]

    # Seed data for DocumentStatus table
    document_status_seed_data = []
    content_hashes = ['hash1', 'hash2', 'hash3', 'hash4', 'hash5']
    metadata_hashes = ['hash6', 'hash7', 'hash8', 'hash9', 'hash10']
    for metadata in document_metadata_seed_data:
        document_status_seed_data.append({
            'customerId': metadata['customerId'],
            'documentId': metadata['documentId'],
            'documentContentHash': random.choice(content_hashes),
            'documentMetadataHash': random.choice(metadata_hashes),
            'ingestionStatus': random.choice(list(DocumentStatusEnum)),
            'extractionStatus': random.choice(list(DocumentStatusEnum)),
            'logs': None
        })
    with app.app_context():
        # Create DocumentMetadata and DocumentStatus objects and add to session
        for metadata_data in document_metadata_seed_data:
            document_metadata = DocumentMetadata(**metadata_data)
            db.session.add(document_metadata)

        for status_data in document_status_seed_data:
            document_status = DocumentStatus(**status_data)
            db.session.add(document_status)

        # Commit changes to the database
        db.session.commit()

    return  jsonify({'message': "Seed Successfully","status":201 })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



