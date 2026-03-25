import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Typography, InputNumber } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import './Models.css'

const { Title } = Typography
const { Option } = Select

interface Model {
  id: string
  name: string
  type: 'local' | 'external'
  status: 'active' | 'inactive'
  description: string
  config: Record<string, any>
  created_at: string
  updated_at: string
}

function Models() {
  const [models, setModels] = useState<Model[]>([])
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [currentModel, setCurrentModel] = useState<Model | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    const mockData: Model[] = [
      {
        id: '1',
        name: '本地目标检测模型',
        type: 'local',
        status: 'active',
        description: '本地部署的目标检测模型',
        config: { model_path: '/path/to/model.pt', confidence_threshold: 0.5 },
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        name: '外部人脸识别API',
        type: 'external',
        status: 'active',
        description: '调用外部人脸识别API',
        config: { api_key: 'api_key', endpoint: 'https://api.example.com/face' },
        created_at: '2023-12-01T11:00:00Z',
        updated_at: '2023-12-01T11:00:00Z'
      }
    ]
    setModels(mockData)
  }, [])

  const showAddModal = () => {
    setIsEditing(false)
    setCurrentModel(null)
    form.resetFields()
    setIsModalVisible(true)
  }

  const showEditModal = (model: Model) => {
    setIsEditing(true)
    setCurrentModel(model)
    form.setFieldsValue(model)
    setIsModalVisible(true)
  }

  const handleOk = () => {
    form.validateFields().then(values => {
      if (isEditing && currentModel) {
        // 更新模型
        const updatedModels = models.map(m => 
          m.id === currentModel.id ? { ...m, ...values } : m
        )
        setModels(updatedModels)
        message.success('模型更新成功')
      } else {
        // 添加模型
        const newModel: Model = {
          id: Date.now().toString(),
          ...values,
          config: {},
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        setModels([...models, newModel])
        message.success('模型添加成功')
      }
      setIsModalVisible(false)
    })
  }

  const handleDelete = (id: string) => {
    const updatedModels = models.filter(m => m.id !== id)
    setModels(updatedModels)
    message.success('模型删除成功')
  }

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => type === 'local' ? '本地' : '外部'
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => status === 'active' ? '活跃' : '非活跃'
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Model) => (
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
            onClick={() => handleDelete(record.id)}
          >
            删除
          </Button>
        </div>
      )
    }
  ]

  return (
    <div className="models-container">
      <div className="page-header">
        <Title level={2}>模型管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={showAddModal}>
          添加模型
        </Button>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={models} 
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={isEditing ? "编辑模型" : "添加模型"}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入模型名称' }]}
          >
            <Input placeholder="请输入模型名称" />
          </Form.Item>
          <Form.Item
            name="type"
            label="类型"
            rules={[{ required: true, message: '请选择模型类型' }]}
          >
            <Select placeholder="请选择模型类型">
              <Option value="local">本地</Option>
              <Option value="external">外部</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择模型状态' }]}
          >
            <Select placeholder="请选择模型状态">
              <Option value="active">活跃</Option>
              <Option value="inactive">非活跃</Option>
            </Select>
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea placeholder="请输入模型描述" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Models
