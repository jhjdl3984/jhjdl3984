db.createCollection("users", { capped: false })
db.users.renameCollection('customers')
db.customers.drop()
db.dropDatabase()
use mongodbtest
db.createCollection('users', { capped: false })
db.users.insertOne({ nama: 'Alice', age: 30, address: ['123 Maple St', '124 Maple St', '125 Maple St'] })
db.users.insertMany([
    { nama: 'Bob', age: 25, address: '456 Oak St' },
    { nama: 'Charlie', age: 35, address: ['789 Pine St', '123 Pine St' ]}
])

db.users.insertOne({ nama: 'John', age: 24, city: 'California'})

db.users.find({}, {nama: 1})

db.users.find()

db.users.find({}, {age: 30, address: 'Maple' })

db.users.updateOne({ nama: 'Alice'}, { $set: { age: 31 } })
db.users.updateMany({ nama: 'Alice' }, { $set: { age: 31 } })
db.users.updateMany({ nama: 'Bob' }, { $set: { age: 100 } })

db.users.deleteOne({ nama: 'Alice' })
db.users.deleteMany({ nama: 'Bob' })

//초급
//생성
db.sports.insertOne({ name: 'Football', players: 11 })

//읽기 $lte: 작거나 같은
db.products.find({ price: { $lte: 500 } })
db.books.find({ author: 'John Doe' })

//업데이트
db.orders.updateMany({ status: 'Pending' }, { $set: { status: 'Complete' } })
db.movies.updateMany({ genre: 'comedy' }, { $set: { rating: 5 } })

//삭제
db.customers.deleteMany({ age: { $lt: 30 } })

//중급
//생성
db.myCollection.insertOne({ name: 'Gadget', type: 'Electronics', price: 300, ratings: [4, 5, 5] })

//읽기 $gte: 크거나 같은
db.employees.find({ department: 'Sales', age: { $gte: 30 } })
db.employees.find({ salary: { $gte: 50000 } }, { name: 1, title: 1 })

//업데이트 값의 존재여부 => $exists:
db.products.updateMany({ stock: { $exists: false } }, { $set: { stock: 10 } })
db.vehicles.updateMany({ type: 'car' }, { $set: { wheels: 4 } })

//삭제
db.orders.deleteMany({ orderDate: { $lt: new Date('2023-01-01') } })
db.restaurants.deleteMany({ rating: { $lt: 3 } })

//고급
//읽기 정렬 => .sort / 1 => 오름차순
db.customeers.find({ age: { $gte: 30 } }).sort({ name: 1 })
//집계 함수 => aggregate() => 여러 안계를 순서대로 처리
//$grooup => 문서를 묶어서 새로운 문서를 만들어 내는 단계
//_id: null => 모든 문서를 하나로 묶음(전체 컬렉션을 집계 대상으로 사용)
//$group에서는 무조건 _id 필드를 써야함
//집계 연산자에서 필드 값 참조할 때 $ 사용 => $age
db.users.aggregate([
    {
        $match:
            {
              birthdate: { $lt: new Date('1990-01-01') }
             }
    },
    {
        $group:
        {
            _id: null, avgAge: { $avg: '$age' }
        }
    }
])

//업데이트
db.employees.updateMany({ department: "HR" }, {$set: { department: 'Human Resources', title: "HR Manager" } })
db.orders.updateMany({ delivered: false }, { $set: { deliveryDate: new Date() } })

//삭제 날짜에서는 기준 날짜 최근 => $gt / 오래된 => $lt
//안쪽 new Date() => 현재 날짜와 시간을 가져옴
//Date - Number => 현재 날짜를 밀리초로 바꿔서 Number와 뺌
//바깥쪽 new Date() => 계산한 밀리초 숫자를 Date로 변환
//밀리초는 => 기준날짜 * 1일을 24시간으로 * 1시간을 60분으로 * 1분을 60초로 * 1초를 밀리초로
db.products.deleteMany({ lastModified: { $lt: new Date(new Date() - 30 * 24 * 60 * 60 * 1000) } })
db.products.deleteMany({ stock: 0 })

db.products.find({ price: { $gt: 100 } })

db.employees.find({ $or: [{ age: { $lt: 30 } }, { department: "HR" }] })

db.orders.find({ quantity: { $gte: 5, $lte: 10 } })

// $not을 쓰려면 다른 연산자($gt, $lte등)와 함께 써야함 => { $not: { $eq: 'Seoul' } }
db.customers.find({ city: { $ne: 'Seoul' } })

db.movies.find({
    rating: { $gte: 8 }, 
    genre: { $in: ['comedy', 'drama'] }
    })

db.books.find({
    author: "John Doe",
    publishedYear: { $gt: 2000 }
})

db.vehicles.find({
    type: { $ne: 'car' },
    price: { $gt: 20000 }
})

db.restaurants.find({
    rating: 5,
    cuisine: { $nin: ["Italian", "French"] }
})

db.users.find({
    age: { $gte: 30 },
    city: { $ne: "New York" }
})

// $and 나 $or => [ {조건1}, {조건2} ]
// $and 없이 => {조건1, 조건2}
db.flights.find({
    $or: [ {departure: "London"}, {arrival: "Tokyo"} ]
})

db.collection.aggregate([
        { $match: { age: { $gte: 30 } } }
])

db.collection.aggregate([
        { $group: { _id: '$department', averageSalary: { $avg: '$salary' } } }
])

db.collection.aggregate([
        { $project: { name: 1, age: 1 } }
])

db.collection.aggregate([
        { $sort: { age: 1 } }
])

db.collection.aggregate([
        { $limit: 5 }
])

db.collection.aggregate([
        { $skip: 10 }
])

db.collection.aggregate([
        { $unwind: '$interests' }
])
// [ { _id: 1, name: "Alice", interests: ["soccer", "music"] } ]
// => [ { _id: 1, name: "Alice", interests: "soccer" },
//      { _id: 1, name: "Alice", interests: "music" } ]

db.orders.aggregate([
        { $lookup: { 
                     from: 'customers',
                     localField: 'customerId',
                     foreigField: '_id',
                     as: 'customerDetails'
                    }
        }
])
// 결과값은 [ {orders컬렉션 값1, as명: [{customers컬렉션 값1}] } ]