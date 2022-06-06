// Code generated by protoc-gen-go-grpc. DO NOT EDIT.

package proto

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// FeatureClient is the client API for Feature service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type FeatureClient interface {
	TrainingData(ctx context.Context, in *TrainingDataRequest, opts ...grpc.CallOption) (Feature_TrainingDataClient, error)
	FeatureServe(ctx context.Context, in *FeatureServeRequest, opts ...grpc.CallOption) (*FeatureRow, error)
}

type featureClient struct {
	cc grpc.ClientConnInterface
}

func NewFeatureClient(cc grpc.ClientConnInterface) FeatureClient {
	return &featureClient{cc}
}

func (c *featureClient) TrainingData(ctx context.Context, in *TrainingDataRequest, opts ...grpc.CallOption) (Feature_TrainingDataClient, error) {
	stream, err := c.cc.NewStream(ctx, &Feature_ServiceDesc.Streams[0], "/featureform.serving.proto.Feature/TrainingData", opts...)
	if err != nil {
		return nil, err
	}
	x := &featureTrainingDataClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type Feature_TrainingDataClient interface {
	Recv() (*TrainingDataRow, error)
	grpc.ClientStream
}

type featureTrainingDataClient struct {
	grpc.ClientStream
}

func (x *featureTrainingDataClient) Recv() (*TrainingDataRow, error) {
	m := new(TrainingDataRow)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

func (c *featureClient) FeatureServe(ctx context.Context, in *FeatureServeRequest, opts ...grpc.CallOption) (*FeatureRow, error) {
	out := new(FeatureRow)
	err := c.cc.Invoke(ctx, "/featureform.serving.proto.Feature/FeatureServe", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// FeatureServer is the server API for Feature service.
// All implementations must embed UnimplementedFeatureServer
// for forward compatibility
type FeatureServer interface {
	TrainingData(*TrainingDataRequest, Feature_TrainingDataServer) error
	FeatureServe(context.Context, *FeatureServeRequest) (*FeatureRow, error)
	mustEmbedUnimplementedFeatureServer()
}

// UnimplementedFeatureServer must be embedded to have forward compatible implementations.
type UnimplementedFeatureServer struct {
}

func (UnimplementedFeatureServer) TrainingData(*TrainingDataRequest, Feature_TrainingDataServer) error {
	return status.Errorf(codes.Unimplemented, "method TrainingData not implemented")
}
func (UnimplementedFeatureServer) FeatureServe(context.Context, *FeatureServeRequest) (*FeatureRow, error) {
	return nil, status.Errorf(codes.Unimplemented, "method FeatureServe not implemented")
}
func (UnimplementedFeatureServer) mustEmbedUnimplementedFeatureServer() {}

// UnsafeFeatureServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to FeatureServer will
// result in compilation errors.
type UnsafeFeatureServer interface {
	mustEmbedUnimplementedFeatureServer()
}

func RegisterFeatureServer(s grpc.ServiceRegistrar, srv FeatureServer) {
	s.RegisterService(&Feature_ServiceDesc, srv)
}

func _Feature_TrainingData_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(TrainingDataRequest)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(FeatureServer).TrainingData(m, &featureTrainingDataServer{stream})
}

type Feature_TrainingDataServer interface {
	Send(*TrainingDataRow) error
	grpc.ServerStream
}

type featureTrainingDataServer struct {
	grpc.ServerStream
}

func (x *featureTrainingDataServer) Send(m *TrainingDataRow) error {
	return x.ServerStream.SendMsg(m)
}

func _Feature_FeatureServe_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(FeatureServeRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(FeatureServer).FeatureServe(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/featureform.serving.proto.Feature/FeatureServe",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(FeatureServer).FeatureServe(ctx, req.(*FeatureServeRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// Feature_ServiceDesc is the grpc.ServiceDesc for Feature service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var Feature_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "featureform.serving.proto.Feature",
	HandlerType: (*FeatureServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "FeatureServe",
			Handler:    _Feature_FeatureServe_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "TrainingData",
			Handler:       _Feature_TrainingData_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "proto/serving.proto",
}