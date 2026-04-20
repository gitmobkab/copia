from inspect import signature, Parameter, Signature
from typing import get_args, get_origin, Literal, Callable, Any

from copia.parser.models import GeneratorCall, POSITIONALS, NAMED, TYPES
from .models import NormalizedSignature
from .exceptions import (
    UnknownGeneratorException,
    TooManyPositionalsException,
    UnknownNamedParamException,
    TypeMismatchException,
    MissingRequiredParamException,
    PositionalNamedCollisionException
)

class SemanticValidator:
    def __init__(self, registry: dict[str, Callable]):
        self.registry = registry

    def validate(self, call: GeneratorCall) -> None:
        if call.name not in self.registry:
            raise UnknownGeneratorException(
                f"Unknown generator: '{call.name}'"
            )

        function_call = self.registry[call.name]
        function_signature = self._normalize(signature(function_call))
        # Our only source of truth to test the positionals and named

        positionals = call.params.positionals
        named = call.params.named
        
        
        if function_signature.var_positional is None:
            self._check_too_many_positionals(call.name, positionals, function_signature)
            self._check_positionals_named_collision(call.name, positionals, named, function_signature)
        
        self._check_unknown_named(call.name, named, function_signature)
        self._check_positional_types(call.name, positionals, function_signature)
        self._check_named_types(call.name, named, function_signature)
        self._check_missing_required(call.name, positionals, named, function_signature)

    # --- Checks ---
    
    def _normalize(self, function_signature: Signature) -> NormalizedSignature:
        positional_or_keyword: list[Parameter] = []
        var_positional: Parameter | None = None
        keyword_only: dict[str, Parameter] = {}
        
        for param in function_signature.parameters.values():
            if param.kind is Parameter.POSITIONAL_OR_KEYWORD:
                positional_or_keyword.append(param)
            elif param.kind is Parameter.VAR_POSITIONAL:
                var_positional = param
            elif param.kind is Parameter.KEYWORD_ONLY:
                keyword_only[param.name] = param
                
        return NormalizedSignature(
            positional_or_keyword,
            var_positional,
            keyword_only
        )

    def _check_too_many_positionals(self, name: str, positionals: POSITIONALS, normalized_signature: NormalizedSignature) -> None:
        """
        Check if there's too many positionals arguments for the generator call
        raise `TooManyPositionalsException` if so
        do nothing otherwise
        """
        if len(positionals) > len(normalized_signature.normals_args):
            raise TooManyPositionalsException(
                f"'{name}' expects at most {len(normalized_signature.normals_args)} positional(s), "
                f"got {len(positionals)}"
            )

    def _check_unknown_named(self, name: str, named: NAMED, normalized_signature: NormalizedSignature) -> None:
        """
        Check if one of the named key is not in the actual parameters of the generator
        raise `UnknownNamedParamException` if so
        do nothing otherwise
        """
        
        for key in named:
            if key not in normalized_signature.by_name :
                raise UnknownNamedParamException(
                    f"'{name}' has no parameter '{key}'"
                )

    def _check_positional_types(self, name: str, positionals: POSITIONALS, normalized_signature: NormalizedSignature):
        """
        Check if the positinals types are in the correct order for the list of parameters
        Skip parameter without a type declaration
        raise `TypeMismatchException` if two types don't match
        do nothing otherwise
        """
        for i, value in enumerate(positionals):
            if i >= len(normalized_signature.normals_args):
                break # assume, the rest is going to *args
            param = normalized_signature.normals_args[i]
            if param.annotation is Parameter.empty:
                continue
            self._assert_type(name, param.name, param.annotation, value)

    def _check_named_types(self, name: str, named: NAMED, normalized_signature: NormalizedSignature):
        """
        Check if the named types are in the correct order for the parameters
        Skip parameter without a type declaration
        raise `TypeMismatchException` if two types don't match
        do nothing otherwise
        """
        for key, value in named.items():
            param = normalized_signature.by_name[key]
            if param.annotation is Parameter.empty:
                continue
            self._assert_type(name, key, param.annotation, value)

    def _check_missing_required(self, name: str, positionals: POSITIONALS, named: NAMED, normalized_signature: NormalizedSignature):
        covered: set[str] = set()
        
        minimum_len = min(len(positionals), len(normalized_signature.normals_args))
        for index in range(minimum_len):
            param = normalized_signature.normals_args[index]
            covered.add(param.name)
        covered |= set(named.keys())
        
        all_params = normalized_signature.normals_args + list(normalized_signature.keywords_only.values())
        
        for param in all_params:
            if (
                param.name not in covered
                and param.default is Parameter.empty
            ):
                raise MissingRequiredParamException(
                    f"'{name}' missing required parameter '{param.name}'"
                )
                
    def _check_positionals_named_collision(self, name: str, positionals: POSITIONALS, named: NAMED, normalized_signature: NormalizedSignature) -> None:
        """
        Check if a named param collides with an already covered positional.
        raise `PositionalNamedCollisionException` if so,
        do nothing otherwise.
        
        IMPORTANT this checker assume that the positionals
        """
        covered_by_positionals: set[str] = set()
        positionals_len = len(positionals)

        for index in range(positionals_len):
            param = normalized_signature.normals_args[index]
            covered_by_positionals.add(param.name)

        for key in named:
            if key in covered_by_positionals:
                raise PositionalNamedCollisionException(
                    f"'{name}' parameter '{key}' is already covered by a positional"
                )

    # --- Type assertion ---

    def _assert_type(self, gen_name: str, param_name: str, annotation: Any, value: TYPES):
        """
        Check if value is the correct type for annotation,
        Literal type is supported.
        
        raise `TypeMismatchException` is the types don't match,
        do nothing otherwise
        """
        origin = get_origin(annotation)

        if origin is Literal:
            allowed = get_args(annotation)
            if value not in allowed:
                raise TypeMismatchException(
                    f"'{gen_name}.{param_name}' must be one of {allowed}, "
                    f"got {value!r}"
                )
        else:
            if not isinstance(value, annotation):
                raise TypeMismatchException(
                    f"'{gen_name}.{param_name}' expects {annotation.__name__}, "
                    f"got {type(value).__name__}"
                )