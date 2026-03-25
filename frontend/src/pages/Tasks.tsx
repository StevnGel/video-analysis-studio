import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Typography } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, PlayCircleOutlined, PauseCircleOutlined, StopOutlined } from '@ant-design/icons'
import './Tasks.css'

const { Title } = Typography
const { Option } = Select

interface Task {
  id: string
  name: string
  video_source_id: string
  model_id: string
  status: 'pending' | 'running' | 'paused' | 'completed' | 'failed'
  description: string
  config: Record<string, any>
  created_at: string
  updated_at: string
  started_at?: string
  completed_at?: string
}

function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [currentTask, setCurrentTask] = useState<Task | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    const mockData: Task[] = [
      {
        id: '1',
        name: '视频目标检测',
        video_source_id: '1',
        model_id: '1',
        status: 'running',
        description: '对本地视频文件进行目标检测',
        config: { interval: 1000 },
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z',
        started_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        name: '视频人脸识别',
        video_source_id: '2',
        model_id: '2',
        status: 'pending',
        description: '对 RTSP 流进行人脸识别',
        config: { interval: 2000 },
        created_at: '2023-12-01T11:00:00Z',
        updated_at: '2023-12-01T11:00:00Z'
      }
    ]
    setTasks(mockData)
  }, [])

  const showAddModal = () => {
    setIsEditing(false)
    setCurrentTask(null)
    form.resetFields()
    setIsModalVisible(true)
  }

  const showEditModal = (task: Task) => {
    setIsEditing(true)
    setCurrentTask(task)
    form.setFieldsValue(task)
    setIsModalVisible(true)
  }

  const handleOk = () => {
    form.validateFields().then(values => {
      if (isEditing && currentTask) {
        // 更新任务
        const updatedTasks = tasks.map(t => 
          t.id === currentTask.id ? { ...t, ...values } : t
        )
        setTasks(updatedTasks)
        message.success('任务更新成功')
      } else {
        // 添加任务
        const newTask: Task = {
          id: Date.now().toString(),
          ...values,
          config: {},
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        setTasks([...tasks, newTask])
        message.success('任务添加成功')
      }
      setIsModalVisible(false)
    })
  }

  const handleDelete = (id: string) => {
    const updatedTasks = tasks.filter(t => t.id !== id)
    setTasks(updatedTasks)
    message.success('任务删除成功')
  }

  const handleTaskAction = (id: string, action: string) => {
    let newStatus: Task['status']
    let messageText: string
    
    switch (action) {
      case 'start':
        newStatus = 'running'
        messageText = '任务启动成功'
        break
      case 'pause':
        newStatus = 'paused'
        messageText = '任务暂停成功'
        break
      case 'stop':
        newStatus = 'completed'
        messageText = '任务停止成功'
        break
      default:
        return
    }
    
    const updatedTasks = tasks.map(t => 
      t.id === id ? { 
        ...t, 
        status: newStatus,
        updated_at: new Date().toISOString(),
        ...(action === 'start' && { started_at: new Date().toISOString() }),
        ...(action === 'stop' && { completed_at: new Date().toISOString() })
      } : t
    )
    setTasks(updatedTasks)
    message.success(messageText)
  }

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '视频源',
      dataIndex: 'video_source_id',
      key: 'video_source_id',
      render: (id: string) => `视频源 ${id}`
    },
    {
      title: '模型',
      dataIndex: 'model_id',
      key: 'model_id',
      render: (id: string) => `模型 ${id}`
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        switch (status) {
          case 'pending': return '待处理'
          case 'running': return '运行中'
          case 'paused': return '已暂停'
          case 'completed': return '已完成'
          case 'failed': return '失败'
          default: return status
        }
      }
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Task) => (
        <div>
          <Button
            type="primary"
            icon={<EditOutlined />}
            size="small"
            style={{ marginRight: 8 }}
            onClick={() => showEditModal(record)}
          >
            编辑
          </Button>
          <Button
            danger
            icon={<DeleteOutlined />}
            size="small"
            style={{ marginRight: 8 }}
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
          {record.status === 'pending' && (
            <Button
              icon={<PlayCircleOutlined />}
              size="small"
              style={{ marginRight: 8 }}
              onClick={() => handleTaskAction(record.id, 'start')}
            >
              启动
            </Button>
          )}
          {record.status === 'running' && (
            <Button
              icon={<PauseCircleOutlined />}
              size="small"
              style={{ marginRight: 8 }}
              onClick={() => handleTaskAction(record.id, 'pause')}
            >
              暂停
            </Button>
          )}
          {(record.status === 'running' || record.status === 'paused') && (
            <Button
              icon={<StopOutlined />}
              size="small"
              onClick={() => handleTaskAction(record.id, 'stop')}
            >
              停止
            </Button>
          )}
        </div>
      )
    }
  ]

  return (
    <div className="tasks-container">
      <div className="page-header">
        <Title level={2}>任务管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={showAddModal}>
          添加任务
        </Button>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={tasks} 
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={isEditing ? "编辑任务" : "添加任务"}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入任务名称' }]}
          >
            <Input placeholder="请输入任务名称" />
          </Form.Item>
          <Form.Item
            name="video_source_id"
            label="视频源"
            rules={[{ required: true, message: '请选择视频源' }]}
          >
            <Select placeholder="请选择视频源">
              <Option value="1">视频源 1</Option>
              <Option value="2">视频源 2</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="model_id"
            label="模型"
            rules={[{ required: true, message: '请选择模型' }]}
          >
            <Select placeholder="请选择模型">
              <Option value="1">模型 1</Option>
              <Option value="2">模型 2</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择任务状态' }]}
          >
            <Select placeholder="请选择任务状态">
              <Option value="pending">待处理</Option>
              <Option value="running">运行中</Option>
              <Option value="paused">已暂停</Option>
              <Option value="completed">已完成</Option>
              <Option value="failed">失败</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea placeholder="请输入任务描述" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Tasks
