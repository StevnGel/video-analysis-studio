import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Select, message, Typography, Tag } from 'antd'
import { EditOutlined, DeleteOutlined, EyeOutlined } from '@ant-design/icons'
import './Events.css'

const { Title } = Typography
const { Option } = Select

interface Event {
  id: string
  task_id: string
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  status: 'new' | 'processed' | 'ignored'
  description: string
  data: Record<string, any>
  created_at: string
  updated_at: string
}

function Events() {
  const [events, setEvents] = useState<Event[]>([])
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [currentEvent, setCurrentEvent] = useState<Event | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    const mockData: Event[] = [
      {
        id: '1',
        task_id: '1',
        type: 'object_detection',
        severity: 'medium',
        status: 'new',
        description: '检测到目标',
        data: { class: 'person', confidence: 0.95, location: { x: 100, y: 200, width: 50, height: 100 } },
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        task_id: '1',
        type: 'object_detection',
        severity: 'high',
        status: 'processed',
        description: '检测到可疑目标',
        data: { class: 'car', confidence: 0.9, location: { x: 200, y: 300, width: 100, height: 50 } },
        created_at: '2023-12-01T10:01:00Z',
        updated_at: '2023-12-01T10:02:00Z'
      }
    ]
    setEvents(mockData)
  }, [])

  const showEventModal = (event: Event) => {
    setCurrentEvent(event)
    form.setFieldsValue(event)
    setIsModalVisible(true)
  }

  const handleUpdateStatus = (id: string, status: Event['status']) => {
    const updatedEvents = events.map(e => 
      e.id === id ? { ...e, status, updated_at: new Date().toISOString() } : e
    )
    setEvents(updatedEvents)
    message.success('事件状态更新成功')
  }

  const handleDelete = (id: string) => {
    const updatedEvents = events.filter(e => e.id !== id)
    setEvents(updatedEvents)
    message.success('事件删除成功')
  }

  const columns = [
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => {
        switch (type) {
          case 'object_detection': return '目标检测'
          case 'face_recognition': return '人脸识别'
          default: return type
        }
      }
    },
    {
      title: '严重程度',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => {
        let color = ''
        switch (severity) {
          case 'low': color = 'green'
            break
          case 'medium': color = 'blue'
            break
          case 'high': color = 'orange'
            break
          case 'critical': color = 'red'
            break
        }
        return <Tag color={color}>{severity === 'low' ? '低' : severity === 'medium' ? '中' : severity === 'high' ? '高' : '严重'}</Tag>
      }
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        let color = ''
        switch (status) {
          case 'new': color = 'blue'
            break
          case 'processed': color = 'green'
            break
          case 'ignored': color = 'gray'
            break
        }
        return <Tag color={color}>{status === 'new' ? '新建' : status === 'processed' ? '已处理' : '已忽略'}</Tag>
      }
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: '任务',
      dataIndex: 'task_id',
      key: 'task_id',
      render: (id: string) => `任务 ${id}`
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (time: string) => new Date(time).toLocaleString()
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Event) => (
        <div>
          <Button
            type="primary"
            icon={<EyeOutlined />}
            size="small"
            style={{ marginRight: 8 }}
            onClick={() => showEventModal(record)}
          >
            查看
          </Button>
          <Select
            defaultValue={record.status}
            style={{ width: 100, marginRight: 8 }}
            onChange={(value) => handleUpdateStatus(record.id, value)}
          >
            <Option value="new">新建</Option>
            <Option value="processed">已处理</Option>
            <Option value="ignored">已忽略</Option>
          </Select>
          <Button
            danger
            icon={<DeleteOutlined />}
            size="small"
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </div>
      )
    }
  ]

  return (
    <div className="events-container">
      <div className="page-header">
        <Title level={2}>事件管理</Title>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={events} 
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title="事件详情"
        open={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        footer={null}
      >
        {currentEvent && (
          <div>
            <div className="event-detail-item">
              <strong>类型:</strong> {currentEvent.type === 'object_detection' ? '目标检测' : currentEvent.type === 'face_recognition' ? '人脸识别' : currentEvent.type}
            </div>
            <div className="event-detail-item">
              <strong>严重程度:</strong> {currentEvent.severity === 'low' ? '低' : currentEvent.severity === 'medium' ? '中' : currentEvent.severity === 'high' ? '高' : '严重'}
            </div>
            <div className="event-detail-item">
              <strong>状态:</strong> {currentEvent.status === 'new' ? '新建' : currentEvent.status === 'processed' ? '已处理' : '已忽略'}
            </div>
            <div className="event-detail-item">
              <strong>描述:</strong> {currentEvent.description}
            </div>
            <div className="event-detail-item">
              <strong>任务:</strong> 任务 {currentEvent.task_id}
            </div>
            <div className="event-detail-item">
              <strong>数据:</strong> <pre>{JSON.stringify(currentEvent.data, null, 2)}</pre>
            </div>
            <div className="event-detail-item">
              <strong>创建时间:</strong> {new Date(currentEvent.created_at).toLocaleString()}
            </div>
            <div className="event-detail-item">
              <strong>更新时间:</strong> {new Date(currentEvent.updated_at).toLocaleString()}
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}

export default Events
