import { useState, useEffect } from 'react'
import { Table, Button, Modal, Form, Input, Select, message, Typography, InputNumber } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import './Configs.css'

const { Title } = Typography
const { Option } = Select

interface Config {
  id: string
  key: string
  value: Record<string, any>
  description: string
  category: string
  created_at: string
  updated_at: string
}

function Configs() {
  const [configs, setConfigs] = useState<Config[]>([])
  const [isModalVisible, setIsModalVisible] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [currentConfig, setCurrentConfig] = useState<Config | null>(null)
  const [form] = Form.useForm()

  // 模拟数据
  useEffect(() => {
    const mockData: Config[] = [
      {
        id: '1',
        key: 'system.max_threads',
        value: { value: 4 },
        description: '系统最大线程数',
        category: 'system',
        created_at: '2023-12-01T10:00:00Z',
        updated_at: '2023-12-01T10:00:00Z'
      },
      {
        id: '2',
        key: 'gstreamer.buffer_size',
        value: { value: 1024 },
        description: 'GStreamer 缓冲区大小',
        category: 'gstreamer',
        created_at: '2023-12-01T11:00:00Z',
        updated_at: '2023-12-01T11:00:00Z'
      }
    ]
    setConfigs(mockData)
  }, [])

  const showAddModal = () => {
    setIsEditing(false)
    setCurrentConfig(null)
    form.resetFields()
    setIsModalVisible(true)
  }

  const showEditModal = (config: Config) => {
    setIsEditing(true)
    setCurrentConfig(config)
    form.setFieldsValue(config)
    setIsModalVisible(true)
  }

  const handleOk = () => {
    form.validateFields().then(values => {
      if (isEditing && currentConfig) {
        // 更新配置
        const updatedConfigs = configs.map(c => 
          c.id === currentConfig.id ? { ...c, ...values } : c
        )
        setConfigs(updatedConfigs)
        message.success('配置更新成功')
      } else {
        // 添加配置
        const newValue = {
          value: values.value
        }
        const newConfig: Config = {
          id: Date.now().toString(),
          ...values,
          value: newValue,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        setConfigs([...configs, newConfig])
        message.success('配置添加成功')
      }
      setIsModalVisible(false)
    })
  }

  const handleDelete = (id: string) => {
    const updatedConfigs = configs.filter(c => c.id !== id)
    setConfigs(updatedConfigs)
    message.success('配置删除成功')
  }

  const columns = [
    {
      title: '键',
      dataIndex: 'key',
      key: 'key'
    },
    {
      title: '值',
      dataIndex: 'value',
      key: 'value',
      render: (value: Record<string, any>) => JSON.stringify(value)
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description'
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category'
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: Config) => (
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
    <div className="configs-container">
      <div className="page-header">
        <Title level={2}>配置管理</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={showAddModal}>
          添加配置
        </Button>
      </div>
      
      <Table 
        columns={columns} 
        dataSource={configs} 
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      <Modal
        title={isEditing ? "编辑配置" : "添加配置"}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={() => setIsModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="key"
            label="键"
            rules={[{ required: true, message: '请输入配置键' }]}
          >
            <Input placeholder="请输入配置键，如 system.max_threads" />
          </Form.Item>
          <Form.Item
            name="value"
            label="值"
            rules={[{ required: true, message: '请输入配置值' }]}
          >
            <Input placeholder="请输入配置值" />
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea placeholder="请输入配置描述" />
          </Form.Item>
          <Form.Item
            name="category"
            label="分类"
            rules={[{ required: true, message: '请选择配置分类' }]}
          >
            <Select placeholder="请选择配置分类">
              <Option value="system">系统</Option>
              <Option value="gstreamer">GStreamer</Option>
              <Option value="model">模型</Option>
              <Option value="task">任务</Option>
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Configs
