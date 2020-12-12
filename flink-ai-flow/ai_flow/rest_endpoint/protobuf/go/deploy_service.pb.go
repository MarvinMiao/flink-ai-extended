// Code generated by protoc-gen-go. DO NOT EDIT.
// source: deploy_service.proto

package deploy_service

import (
	context "context"
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	//_ "github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/google/api"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type WorkflowRequest struct {
	Id                   int64    `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	WorkflowJson         string   `protobuf:"bytes,2,opt,name=workflow_json,json=workflowJson,proto3" json:"workflow_json,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *WorkflowRequest) Reset()         { *m = WorkflowRequest{} }
func (m *WorkflowRequest) String() string { return proto.CompactTextString(m) }
func (*WorkflowRequest) ProtoMessage()    {}
func (*WorkflowRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_4f431ac2f5cae27c, []int{0}
}

func (m *WorkflowRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_WorkflowRequest.Unmarshal(m, b)
}
func (m *WorkflowRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_WorkflowRequest.Marshal(b, m, deterministic)
}
func (m *WorkflowRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_WorkflowRequest.Merge(m, src)
}
func (m *WorkflowRequest) XXX_Size() int {
	return xxx_messageInfo_WorkflowRequest.Size(m)
}
func (m *WorkflowRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_WorkflowRequest.DiscardUnknown(m)
}

var xxx_messageInfo_WorkflowRequest proto.InternalMessageInfo

func (m *WorkflowRequest) GetId() int64 {
	if m != nil {
		return m.Id
	}
	return 0
}

func (m *WorkflowRequest) GetWorkflowJson() string {
	if m != nil {
		return m.WorkflowJson
	}
	return ""
}

type ScheduleResponse struct {
	ReturnCode           int64    `protobuf:"varint,1,opt,name=return_code,json=returnCode,proto3" json:"return_code,omitempty"`
	ReturnMsg            string   `protobuf:"bytes,2,opt,name=return_msg,json=returnMsg,proto3" json:"return_msg,omitempty"`
	Data                 string   `protobuf:"bytes,3,opt,name=data,proto3" json:"data,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *ScheduleResponse) Reset()         { *m = ScheduleResponse{} }
func (m *ScheduleResponse) String() string { return proto.CompactTextString(m) }
func (*ScheduleResponse) ProtoMessage()    {}
func (*ScheduleResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_4f431ac2f5cae27c, []int{1}
}

func (m *ScheduleResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_ScheduleResponse.Unmarshal(m, b)
}
func (m *ScheduleResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_ScheduleResponse.Marshal(b, m, deterministic)
}
func (m *ScheduleResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_ScheduleResponse.Merge(m, src)
}
func (m *ScheduleResponse) XXX_Size() int {
	return xxx_messageInfo_ScheduleResponse.Size(m)
}
func (m *ScheduleResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_ScheduleResponse.DiscardUnknown(m)
}

var xxx_messageInfo_ScheduleResponse proto.InternalMessageInfo

func (m *ScheduleResponse) GetReturnCode() int64 {
	if m != nil {
		return m.ReturnCode
	}
	return 0
}

func (m *ScheduleResponse) GetReturnMsg() string {
	if m != nil {
		return m.ReturnMsg
	}
	return ""
}

func (m *ScheduleResponse) GetData() string {
	if m != nil {
		return m.Data
	}
	return ""
}

type MasterConfigRequest struct {
	Id                   int64    `protobuf:"varint,1,opt,name=id,proto3" json:"id,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *MasterConfigRequest) Reset()         { *m = MasterConfigRequest{} }
func (m *MasterConfigRequest) String() string { return proto.CompactTextString(m) }
func (*MasterConfigRequest) ProtoMessage()    {}
func (*MasterConfigRequest) Descriptor() ([]byte, []int) {
	return fileDescriptor_4f431ac2f5cae27c, []int{2}
}

func (m *MasterConfigRequest) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MasterConfigRequest.Unmarshal(m, b)
}
func (m *MasterConfigRequest) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MasterConfigRequest.Marshal(b, m, deterministic)
}
func (m *MasterConfigRequest) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MasterConfigRequest.Merge(m, src)
}
func (m *MasterConfigRequest) XXX_Size() int {
	return xxx_messageInfo_MasterConfigRequest.Size(m)
}
func (m *MasterConfigRequest) XXX_DiscardUnknown() {
	xxx_messageInfo_MasterConfigRequest.DiscardUnknown(m)
}

var xxx_messageInfo_MasterConfigRequest proto.InternalMessageInfo

func (m *MasterConfigRequest) GetId() int64 {
	if m != nil {
		return m.Id
	}
	return 0
}

type MasterConfigResponse struct {
	ReturnCode           int64             `protobuf:"varint,1,opt,name=return_code,json=returnCode,proto3" json:"return_code,omitempty"`
	ReturnMsg            string            `protobuf:"bytes,2,opt,name=return_msg,json=returnMsg,proto3" json:"return_msg,omitempty"`
	Config               map[string]string `protobuf:"bytes,3,rep,name=config,proto3" json:"config,omitempty" protobuf_key:"bytes,1,opt,name=key,proto3" protobuf_val:"bytes,2,opt,name=value,proto3"`
	XXX_NoUnkeyedLiteral struct{}          `json:"-"`
	XXX_unrecognized     []byte            `json:"-"`
	XXX_sizecache        int32             `json:"-"`
}

func (m *MasterConfigResponse) Reset()         { *m = MasterConfigResponse{} }
func (m *MasterConfigResponse) String() string { return proto.CompactTextString(m) }
func (*MasterConfigResponse) ProtoMessage()    {}
func (*MasterConfigResponse) Descriptor() ([]byte, []int) {
	return fileDescriptor_4f431ac2f5cae27c, []int{3}
}

func (m *MasterConfigResponse) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MasterConfigResponse.Unmarshal(m, b)
}
func (m *MasterConfigResponse) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MasterConfigResponse.Marshal(b, m, deterministic)
}
func (m *MasterConfigResponse) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MasterConfigResponse.Merge(m, src)
}
func (m *MasterConfigResponse) XXX_Size() int {
	return xxx_messageInfo_MasterConfigResponse.Size(m)
}
func (m *MasterConfigResponse) XXX_DiscardUnknown() {
	xxx_messageInfo_MasterConfigResponse.DiscardUnknown(m)
}

var xxx_messageInfo_MasterConfigResponse proto.InternalMessageInfo

func (m *MasterConfigResponse) GetReturnCode() int64 {
	if m != nil {
		return m.ReturnCode
	}
	return 0
}

func (m *MasterConfigResponse) GetReturnMsg() string {
	if m != nil {
		return m.ReturnMsg
	}
	return ""
}

func (m *MasterConfigResponse) GetConfig() map[string]string {
	if m != nil {
		return m.Config
	}
	return nil
}

func init() {
	proto.RegisterType((*WorkflowRequest)(nil), "WorkflowRequest")
	proto.RegisterType((*ScheduleResponse)(nil), "ScheduleResponse")
	proto.RegisterType((*MasterConfigRequest)(nil), "MasterConfigRequest")
	proto.RegisterType((*MasterConfigResponse)(nil), "MasterConfigResponse")
	proto.RegisterMapType((map[string]string)(nil), "MasterConfigResponse.ConfigEntry")
}

func init() {
	proto.RegisterFile("deploy_service.proto", fileDescriptor_4f431ac2f5cae27c)
}

var fileDescriptor_4f431ac2f5cae27c = []byte{
	// 481 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xac, 0x93, 0x41, 0x6f, 0xd3, 0x30,
	0x14, 0xc7, 0xe5, 0x76, 0x4c, 0xea, 0x2b, 0x63, 0xc5, 0x74, 0x52, 0x54, 0x01, 0x2b, 0x1e, 0x13,
	0xa5, 0xa0, 0x44, 0x2a, 0x17, 0xd6, 0x1b, 0x8c, 0x71, 0x40, 0xda, 0x25, 0x3b, 0x70, 0x8c, 0x4c,
	0xf2, 0x9a, 0x85, 0xa6, 0x76, 0xb0, 0x9d, 0x8e, 0x5e, 0x39, 0x71, 0x44, 0xe2, 0x9b, 0xf0, 0x39,
	0xb8, 0xf1, 0x15, 0xf8, 0x20, 0x28, 0x76, 0x22, 0x8d, 0xd1, 0x22, 0x84, 0x76, 0xcb, 0x7b, 0xf6,
	0xfb, 0xff, 0x9e, 0xfc, 0xff, 0x07, 0xfa, 0x09, 0x16, 0xb9, 0x5c, 0x45, 0x1a, 0xd5, 0x32, 0x8b,
	0xd1, 0x2f, 0x94, 0x34, 0x72, 0x70, 0x37, 0x95, 0x32, 0xcd, 0x31, 0xe0, 0x45, 0x16, 0x70, 0x21,
	0xa4, 0xe1, 0x26, 0x93, 0x42, 0xbb, 0x53, 0xf6, 0x1a, 0x76, 0xdf, 0x4a, 0x35, 0x9f, 0xe5, 0xf2,
	0x22, 0xc4, 0x0f, 0x25, 0x6a, 0x43, 0x6f, 0x41, 0x2b, 0x4b, 0x3c, 0x32, 0x24, 0xa3, 0x76, 0xd8,
	0xca, 0x12, 0x7a, 0x00, 0x3b, 0x17, 0xf5, 0x95, 0xe8, 0xbd, 0x96, 0xc2, 0x6b, 0x0d, 0xc9, 0xa8,
	0x13, 0xde, 0x6c, 0x9a, 0x6f, 0xb4, 0x14, 0x6c, 0x06, 0xbd, 0xb3, 0xf8, 0x1c, 0x93, 0x32, 0xc7,
	0x10, 0x75, 0x21, 0x85, 0x46, 0xba, 0x0f, 0x5d, 0x85, 0xa6, 0x54, 0x22, 0x8a, 0x65, 0x82, 0xb5,
	0x22, 0xb8, 0xd6, 0xb1, 0x4c, 0x90, 0xde, 0x83, 0xba, 0x8a, 0x16, 0x3a, 0xad, 0x65, 0x3b, 0xae,
	0x73, 0xaa, 0x53, 0x4a, 0x61, 0x2b, 0xe1, 0x86, 0x7b, 0x6d, 0x7b, 0x60, 0xbf, 0xd9, 0x21, 0xdc,
	0x39, 0xe5, 0xda, 0xa0, 0x3a, 0x96, 0x62, 0x96, 0xa5, 0x1b, 0x76, 0x66, 0xdf, 0x09, 0xf4, 0x7f,
	0xbf, 0x77, 0x4d, 0x3b, 0x1d, 0xc1, 0x76, 0x6c, 0x15, 0xbd, 0xf6, 0xb0, 0x3d, 0xea, 0x4e, 0x1e,
	0xf8, 0xeb, 0x30, 0xbe, 0x2b, 0x4f, 0x84, 0x51, 0xab, 0xb0, 0x1e, 0x18, 0x1c, 0x41, 0xf7, 0x52,
	0x9b, 0xf6, 0xa0, 0x3d, 0xc7, 0x95, 0xdd, 0xa0, 0x13, 0x56, 0x9f, 0xb4, 0x0f, 0x37, 0x96, 0x3c,
	0x2f, 0xb1, 0xa6, 0xba, 0x62, 0xda, 0x7a, 0x4e, 0x26, 0xdf, 0xb6, 0x60, 0xe7, 0x95, 0x35, 0xf7,
	0xcc, 0x79, 0x4b, 0xcf, 0x61, 0x4f, 0x1b, 0xae, 0x4c, 0xf3, 0xe8, 0x8d, 0x89, 0xb4, 0xe7, 0x5f,
	0xf1, 0x73, 0x70, 0xdb, 0xbf, 0xea, 0x0c, 0x1b, 0x7f, 0xfa, 0xf1, 0xf3, 0x6b, 0xeb, 0x21, 0xdb,
	0x0f, 0x78, 0x56, 0x5d, 0x0d, 0x5c, 0x72, 0x50, 0x05, 0x8d, 0xa9, 0x81, 0x55, 0x9f, 0x92, 0x31,
	0x9d, 0x41, 0x5f, 0x1b, 0x59, 0xfc, 0x1f, 0xe8, 0xb1, 0x05, 0x1d, 0xb0, 0xfb, 0x7f, 0x03, 0xc9,
	0xa2, 0xe2, 0x08, 0x18, 0xa4, 0x68, 0x1a, 0xcd, 0x93, 0x8f, 0x18, 0x97, 0x55, 0x50, 0x43, 0xd4,
	0x65, 0x6e, 0xfe, 0x8d, 0xf6, 0xc4, 0xd2, 0x0e, 0xd9, 0x70, 0x33, 0x4d, 0x59, 0xb9, 0x8a, 0x37,
	0x07, 0x2f, 0xd3, 0x7f, 0xe0, 0x5e, 0xe4, 0xd9, 0x12, 0xaf, 0xed, 0x11, 0x79, 0xa5, 0x56, 0xc1,
	0x14, 0xec, 0xa6, 0x68, 0x2e, 0x47, 0x85, 0xf6, 0xfd, 0x35, 0x41, 0x1e, 0xec, 0xad, 0xcd, 0x13,
	0x9b, 0x58, 0xd6, 0x53, 0xf6, 0x68, 0x33, 0x6b, 0x61, 0xe7, 0x22, 0x17, 0xb6, 0x29, 0x19, 0xbf,
	0xf4, 0xa0, 0x17, 0xcb, 0x85, 0xef, 0x06, 0xdc, 0xef, 0xfe, 0x99, 0x90, 0x2f, 0x84, 0xbc, 0xdb,
	0xb6, 0xc5, 0xb3, 0x5f, 0x01, 0x00, 0x00, 0xff, 0xff, 0x75, 0x74, 0xde, 0xb0, 0x31, 0x04, 0x00,
	0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConnInterface

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion6

// DeployServiceClient is the client API for DeployService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type DeployServiceClient interface {
	StartScheduleWorkflow(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error)
	StopScheduleWorkflow(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error)
	GetWorkflowExecutionResult(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error)
	IsWorkflowExecutionAlive(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error)
	GetMasterConfig(ctx context.Context, in *MasterConfigRequest, opts ...grpc.CallOption) (*MasterConfigResponse, error)
}

type deployServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewDeployServiceClient(cc grpc.ClientConnInterface) DeployServiceClient {
	return &deployServiceClient{cc}
}

func (c *deployServiceClient) StartScheduleWorkflow(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error) {
	out := new(ScheduleResponse)
	err := c.cc.Invoke(ctx, "/DeployService/startScheduleWorkflow", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *deployServiceClient) StopScheduleWorkflow(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error) {
	out := new(ScheduleResponse)
	err := c.cc.Invoke(ctx, "/DeployService/stopScheduleWorkflow", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *deployServiceClient) GetWorkflowExecutionResult(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error) {
	out := new(ScheduleResponse)
	err := c.cc.Invoke(ctx, "/DeployService/getWorkflowExecutionResult", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *deployServiceClient) IsWorkflowExecutionAlive(ctx context.Context, in *WorkflowRequest, opts ...grpc.CallOption) (*ScheduleResponse, error) {
	out := new(ScheduleResponse)
	err := c.cc.Invoke(ctx, "/DeployService/isWorkflowExecutionAlive", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *deployServiceClient) GetMasterConfig(ctx context.Context, in *MasterConfigRequest, opts ...grpc.CallOption) (*MasterConfigResponse, error) {
	out := new(MasterConfigResponse)
	err := c.cc.Invoke(ctx, "/DeployService/getMasterConfig", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// DeployServiceServer is the server API for DeployService service.
type DeployServiceServer interface {
	StartScheduleWorkflow(context.Context, *WorkflowRequest) (*ScheduleResponse, error)
	StopScheduleWorkflow(context.Context, *WorkflowRequest) (*ScheduleResponse, error)
	GetWorkflowExecutionResult(context.Context, *WorkflowRequest) (*ScheduleResponse, error)
	IsWorkflowExecutionAlive(context.Context, *WorkflowRequest) (*ScheduleResponse, error)
	GetMasterConfig(context.Context, *MasterConfigRequest) (*MasterConfigResponse, error)
}

// UnimplementedDeployServiceServer can be embedded to have forward compatible implementations.
type UnimplementedDeployServiceServer struct {
}

func (*UnimplementedDeployServiceServer) StartScheduleWorkflow(ctx context.Context, req *WorkflowRequest) (*ScheduleResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StartScheduleWorkflow not implemented")
}
func (*UnimplementedDeployServiceServer) StopScheduleWorkflow(ctx context.Context, req *WorkflowRequest) (*ScheduleResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method StopScheduleWorkflow not implemented")
}
func (*UnimplementedDeployServiceServer) GetWorkflowExecutionResult(ctx context.Context, req *WorkflowRequest) (*ScheduleResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetWorkflowExecutionResult not implemented")
}
func (*UnimplementedDeployServiceServer) IsWorkflowExecutionAlive(ctx context.Context, req *WorkflowRequest) (*ScheduleResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method IsWorkflowExecutionAlive not implemented")
}
func (*UnimplementedDeployServiceServer) GetMasterConfig(ctx context.Context, req *MasterConfigRequest) (*MasterConfigResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetMasterConfig not implemented")
}

func RegisterDeployServiceServer(s *grpc.Server, srv DeployServiceServer) {
	s.RegisterService(&_DeployService_serviceDesc, srv)
}

func _DeployService_StartScheduleWorkflow_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(WorkflowRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DeployServiceServer).StartScheduleWorkflow(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/DeployService/StartScheduleWorkflow",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DeployServiceServer).StartScheduleWorkflow(ctx, req.(*WorkflowRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _DeployService_StopScheduleWorkflow_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(WorkflowRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DeployServiceServer).StopScheduleWorkflow(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/DeployService/StopScheduleWorkflow",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DeployServiceServer).StopScheduleWorkflow(ctx, req.(*WorkflowRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _DeployService_GetWorkflowExecutionResult_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(WorkflowRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DeployServiceServer).GetWorkflowExecutionResult(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/DeployService/GetWorkflowExecutionResult",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DeployServiceServer).GetWorkflowExecutionResult(ctx, req.(*WorkflowRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _DeployService_IsWorkflowExecutionAlive_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(WorkflowRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DeployServiceServer).IsWorkflowExecutionAlive(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/DeployService/IsWorkflowExecutionAlive",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DeployServiceServer).IsWorkflowExecutionAlive(ctx, req.(*WorkflowRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _DeployService_GetMasterConfig_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MasterConfigRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(DeployServiceServer).GetMasterConfig(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/DeployService/GetMasterConfig",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(DeployServiceServer).GetMasterConfig(ctx, req.(*MasterConfigRequest))
	}
	return interceptor(ctx, in, info, handler)
}

var _DeployService_serviceDesc = grpc.ServiceDesc{
	ServiceName: "DeployService",
	HandlerType: (*DeployServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "startScheduleWorkflow",
			Handler:    _DeployService_StartScheduleWorkflow_Handler,
		},
		{
			MethodName: "stopScheduleWorkflow",
			Handler:    _DeployService_StopScheduleWorkflow_Handler,
		},
		{
			MethodName: "getWorkflowExecutionResult",
			Handler:    _DeployService_GetWorkflowExecutionResult_Handler,
		},
		{
			MethodName: "isWorkflowExecutionAlive",
			Handler:    _DeployService_IsWorkflowExecutionAlive_Handler,
		},
		{
			MethodName: "getMasterConfig",
			Handler:    _DeployService_GetMasterConfig_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "deploy_service.proto",
}