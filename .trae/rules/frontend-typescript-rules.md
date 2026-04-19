# 前端 TypeScript 开发规则

## 代码风格

### 缩进和空格
- 使用 2 个空格进行缩进
- 每行长度不超过 120 个字符
- 文件末尾保留一个空行

### 命名约定
- **变量和函数**: 使用小驼峰命名法（camelCase）
- **常量**: 使用大驼峰命名法（PascalCase）或全大写蛇形命名法（SNAKE_CASE）
- **组件**: 使用大驼峰命名法（PascalCase）
- **接口和类型**: 使用大驼峰命名法（PascalCase），并以 `I` 或 `T` 开头

### 类型定义
- 优先使用接口（interface）定义对象类型
- 当需要联合类型或交叉类型时，使用类型别名（type）
- 避免使用 `any` 类型，尽量使用更具体的类型

### 导入和导出
- 使用 ES6 模块语法（import/export）
- 按以下顺序组织导入：
  1. 外部依赖
  2. 内部组件
  3. 样式文件
- 导出时，优先使用默认导出（export default）还是命名导出（export）取决于模块的用途

## 组件开发

### 组件结构
- 每个组件放在单独的文件中
- 组件文件命名与组件名称一致
- 对于复杂组件，可创建对应的文件夹，包含组件文件和相关文件

### 状态管理
- 使用 React Hooks 管理组件状态
- 对于全局状态，使用 Context API 或状态管理库
- 保持状态逻辑清晰，避免过度复杂的状态管理

### Props 类型
- 使用 TypeScript 接口定义组件 Props 类型
- 为 Props 添加适当的类型注解和默认值
- 对于可选 Props，使用 `?` 标记

### 样式管理
- 使用 CSS Modules 或 styled-components 管理组件样式
- 避免使用全局样式，优先使用局部样式
- 保持样式代码简洁，避免过度嵌套

## 代码质量

### 代码审查
- 定期进行代码审查，确保代码质量
- 关注代码的可读性、可维护性和性能
- 避免重复代码，提取可复用的逻辑

### 测试
- 为组件和关键功能编写单元测试
- 使用 Jest 和 React Testing Library 进行测试
- 确保测试覆盖率达到合理水平

### 错误处理
- 合理处理错误，避免应用崩溃
- 使用 try-catch 捕获可能的错误
- 为用户提供清晰的错误提示

## 性能优化

### 渲染优化
- 使用 React.memo 优化组件渲染
- 合理使用 useCallback 和 useMemo 缓存函数和计算结果
- 避免在渲染过程中进行复杂计算

### 网络优化
- 使用适当的 HTTP 缓存策略
- 合理使用防抖和节流技术
- 考虑使用 GraphQL 或其他高效的 API 设计

## 项目结构

### 目录结构
- `src/components`: 组件
- `src/pages`: 页面
- `src/hooks`: 自定义 Hooks
- `src/utils`: 工具函数
- `src/services`: API 服务
- `src/types`: 类型定义
- `src/assets`: 静态资源

### 文件命名
- 组件文件: `ComponentName.tsx`
- 类型文件: `types.ts` 或 `interface.ts`
- 工具文件: `util.ts` 或 `helper.ts`
- 样式文件: `ComponentName.module.css` 或 `ComponentName.css`

## 工具和配置

### 开发工具
- 使用 VS Code 作为主要开发工具
- 安装必要的扩展，如 ESLint、Prettier、TypeScript 等

### 配置文件
- `tsconfig.json`: TypeScript 配置
- `eslint.config.js`: ESLint 配置
- `prettier.config.js`: Prettier 配置
- `vite.config.ts`: Vite 配置

### 脚本命令
- `npm run dev`: 启动开发服务器
- `npm run build`: 构建生产版本
- `npm run lint`: 运行 ESLint 检查
- `npm run test`: 运行测试

## 最佳实践

- 遵循 React 官方推荐的最佳实践
- 保持代码简洁，避免过度工程化
- 注重代码的可读性和可维护性
- 定期更新依赖，确保使用最新的稳定版本
- 编写清晰的文档，便于团队协作