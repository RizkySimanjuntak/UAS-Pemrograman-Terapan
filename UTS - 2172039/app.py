from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///data.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    stok = Column(Integer)
    harga = Column(Integer)

class tabelLog(Base):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    item_id = Column(Integer)
    name = Column(String(100))
    stok_lama = Column(Integer)
    stok_baru = Column(Integer)
    harga_lama = Column(Integer)
    harga_baru = Column(Integer)

Base.metadata.create_all(engine)

def get_session():
    return Session()

@app.route('/')
def index():
    session = get_session()
    data = session.query(Item).all()
    session.close()
    return render_template('index.html', data=data)

@app.route('/log')
def log():
    session = get_session()
    log_data = session.query(tabelLog).all()
    session.close()
    return render_template('log.html', log_data=log_data)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        session = get_session()
        name = request.form['name']
        stok = request.form['stok']
        harga = request.form['harga']
        barang_baru = Item(name=name, stok=stok, harga=harga)
        session.add(barang_baru)
        session.commit()
        session.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    session = get_session()
    item = session.query(Item).filter_by(id=id).first()
    if request.method == 'POST':
        if item:
            stok_lama = item.stok
            harga_lama = item.harga
            item.name = request.form['name']
            item.stok = request.form['stok']
            item.harga = request.form['harga']
            log_entry = tabelLog(item_id=item.id, name=item.name, stok_lama=stok_lama, stok_baru=item.stok,
                                 harga_lama=harga_lama, harga_baru=item.harga)
            session.add(log_entry)
            session.commit()
            session.close()
            return redirect(url_for('index'))
    session.close()
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    session = get_session()
    item = session.query(Item).filter_by(id=id).first()
    if item:
        session.delete(item)
        session.commit()
    session.close()
    return redirect(url_for('index'))

@app.route('/log/delete/<int:id>')
def delete_log(id):
    session = get_session()
    log_entry = session.query(tabelLog).filter_by(id=id).first()
    if log_entry:
        session.delete(log_entry)
        session.commit()
    session.close()
    return redirect(url_for('log'))

if __name__ == '__main__':
    app.run(debug=True)
