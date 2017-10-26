# -*- coding: utf-8 -*-
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
    r"""
        # From J3/04-007(Fortran 2003)
        program                 = program_unit+
        program_unit            = main_program / external_subprogram / module /
                                  block_data / _C / _L
        main_program            = program_stmt? specification_part? execution_part?
                                  internal_subprogram_part? end_program_stmt
        external_subprogram     = function_subprogram / subroutine_subprogram
        function_subprogram     = function_stmt specification_part? execution_part?
                                  internal_subprogram_part? end_function_stmt
        subroutine_subprogram   = subroutine_stmt specification_part?
                                  execution_part? internal_subprogram_part?
                                  end_subroutine_stmt
        module                  = module_stmt specification_part?
                                  module_subprogram_part? end_module_stmt
        block_data              = block_data_stmt specification_part?
                                  end_block_data_stmt
        specification_part      = (use_stmt _C*)*  (import_stmt _C*)*
                                  (implicit_part _C*)* declaration_construct*
        implicit_part           = implicit_stmt / implicit_part_stmt*
        implicit_part_stmt      = implicit_stmt / parameter_stmt /
                                  format_stmt / entry_stmt
        declaration_construct   = derived_type_def / entry_stmt / enum_def /
                                  format_stmt / interface_block / parameter_stmt /
                                  procedure_declaration_stmt / specification_stmt /
                                  type_declaration_stmt / stmt_function_stmt / _C
        execution_part          = executable_construct execution_part_construct*
        execution_part_construct= executable_construct / format_stmt / entry_stmt /
                                  data_stmt / _C
        internal_subprogram_part= contains_stmt _C* (internal_subprogram _C*)+
        internal_subprogram     = function_subprogram / subroutine_subprogram
        module_subprogram_part  = contains_stmt _C* (internal_subprogram _C*)+
        module_subprogram       = function_subprogram / subroutine_subprogram
        specification_stmt      = access_stmt / allocatable_stmt / asynchronous_stmt /
                                  bind_stmt / common_stmt / data_stmt /
                                  dimension_stmt / equivalence_stmt /
                                  external_stmt / intent_stmt / intrinsic_stmt /
                                  namelist_stmt / optional_stmt / pointer_stmt /
                                  protected_stmt / save_stmt / target_stmt /
                                  volatile_stmt / value_stmt
        executable_construct    = action_stmt / associate_construct / case_constructor /
                                  do_construct / forall_construct / if_construct /
                                  select_type_construct / where_construct
        action_stmt             = allocate_stmt / assignment_stmt / backspace_stmt /
                                  call_stmt / close_stmt / continue_stmt / cycle_stmt /
                                  deallocate_stmt / endfile_stmt / exit_stmt /
                                  flush_stmt / forall_stmt / goto_stmt / if_stmt /
                                  inquire_stmt / nullify_stmt / open_stmt /
                                  pointer_assignment_stmt / print_stmt / read_stmt /
                                  return_stmt / rewind_stmt / stop_stmt / wait_stmt /
                                  where_stmt / write_stmt / arithmetic_if_stmt /
                                  computed_goto_stmt

        ################## statements ###################
        program_stmt            = _0 ~"PROGRAM"i _1 program_name _0 EOL
        module_stmt             = "$"
        end_module_stmt         = "$"
        block_data_stmt         = "$"
        end_block_data_stmt     = "$"
        letter                  = ~"[A-Z]"i
        name                    = ~"[A-Z][_A-Z0-9]{0,63}"i
        use_stmt                = "$"
        import_stmt             = "$"
        implicit_stmt           = (_0 ~"IMPLICIT"i _1 implicit_spec_list _0 EOL) /
                                  (_0 ~"IMPLICIT"i _1 ~"NONE"i _0 EOL)
        function_stmt           = _0 (prefix _1)? ~"FUNCTION"i _1 function_name _0
                                  "(" _0 dummy_arg_name_list? _0 ")" (_0 suffix)? _0 EOL
        contains_stmt           = _0 ~"CONTAINS"i _0 EOL
        subroutine_stmt         = _0 prefix? ~"SUBROUTINE"i subroutine_name ("("
                                  dummy_arg_list? ")" proc_language_binding_spec?)? _0 EOL
        procedure_declaration_stmt  = "$"
        access_stmt             = "$"
        allocatable_stmt        = "$"
        asynchronous_stmt       = "$"
        bind_stmt               = "$"
        common_stmt             = "$"
        data_stmt               = "$"
        dimension_stmt          = "$"
        equivalence_stmt        = "$"
        external_stmt           = "$"
        intent_stmt             = "$"
        intrinsic_stmt          = "$"
        namelist_stmt           = "$"
        optional_stmt           = "$"
        pointer_stmt            = "$"
        protected_stmt          = "$"
        save_stmt               = "$"
        target_stmt             = "$"
        volatile_stmt           = "$"
        value_stmt              = "$"
        do_stmt                 = label_do_stmt / nonlabel_do_stmt
        nonlabel_do_stmt        = (_0 do_construct_name _0 ":")? _0 ~"DO"i _0
                                  loop_control? _0 EOL
        end_do_stmt             = _0 ~"END"i _0 ~"DO"i _0 do_construct_name? _0 EOL
        label_do_stmt           = "$"
        allocate_stmt           = "$"
        assignment_stmt         = _0 variable _0 "=" _0 expr _0 EOL
        backspace_stmt          = "$"
        call_stmt               = "$"
        close_stmt              = "$"
        continue_stmt           = _0 ~"CONTINUE"i _0 EOL
        cycle_stmt              = "$"
        deallocate_stmt         = "$"
        endfile_stmt            = "$"
        end_function_stmt       = _0 ~"END"i (_0 ~"FUNCTION"i (_1 function_name)?)? _0 EOL
        end_program_stmt        = _0 ~"END"i (_0 ~"PROGRAM"i (_1 program_name)?)? _0 EOL
        end_subroutine_stmt     = "$"
        exit_stmt               = "$"
        flush_stmt              = "$"
        forall_stmt             = "$"
        goto_stmt               = "$"
        if_stmt                 = "$"
        inquire_stmt            = "$"
        nullify_stmt            = "$"
        open_stmt               = "$"
        pointer_assignment_stmt = "$"
        print_stmt              = _0 ~"PRINT"i _1 format (_0 "," _0 output_item_list)? _0 EOL
        read_stmt               = "$"
        return_stmt             = "$"
        rewind_stmt             = "$"
        stop_stmt               = "$"
        wait_stmt               = "$"
        where_stmt              = "$"
        write_stmt              = "$"
        arithmetic_if_stmt      = "$"
        computed_goto_stmt      = "$"
        stmt_function_stmt      = "$"
        type_declaration_stmt   = _0 declaration_type_spec ((_0 "," _0 attr_spec )* _0 "::" )?
                                  _0 entity_decl_list _0 EOL
        parameter_stmt          = "$"
        format_stmt             = "$"
        entry_stmt              = "$"


        prefix                  = prefix_spec+
        prefix_spec             = ~"RECURSIVE"i / ~"PURE"i / ~"ELEMENTAL"i /
                                  declaration_type_spec
        dummy_arg_name_list     = dummy_arg_name (_0 "," _0 dummy_arg_name)*
        suffix                  = (proc_language_binding_spec (_1 ~"RESULT"i _0 "(" _0
                                  result_name _0 ")")?) / (~"RESULT"i _0 "(" _0
                                  result_name _0 ")" _0 proc_language_binding_spec?)
        proc_language_binding_spec = language_binding_spec
        dummy_arg_list          = dummy_arg (_0 "," _0 dummy_arg)*
        dummy_arg               = "*" / dummy_arg_name
        derived_type_def        = "$"
        enum_def                = "$"
        interface_block         = "$"
        associate_construct     = "$"
        case_constructor        = "$"
        do_construct            = block_do_construct / nonblock_do_construct
        block_do_construct      = do_stmt do_block end_do
        do_block                = block
        block                   = execution_part_construct*
        loop_control            = (","? _0 do_variable _0 "=" _0 scalar_int_expr _0
                                  "," _0 scalar_int_expr (_0 "," _0 scalar_int_expr )?) /
                                  (","? _0 ~"WHILE"i _0 "(" _0 scalar_logical_expr _0 ")")
        do_variable             = scalar_int_variable
        scalar_logical_expr     = logical_expr
        logical_expr            = expr
        end_do                  = end_do_stmt / continue_stmt
        nonblock_do_construct   = "$"
        forall_construct        = "$"
        if_construct            = "$"
        select_type_construct   = "$"
        where_construct         = "$"
        format                  = default_char_expr / label / "*"
        default_char_expr       = expr
        output_item_list        = output_item (_0 "," _0 output_item)*
        output_item             = io_implied_do / expr
        io_implied_do           = "$"
        entity_decl_list        = entity_decl (_0 "," _0 entity_decl)*
        entity_decl             = (object_name (_0 "(" _0 array_spec _0 ")")? (_0 "*" _0
                                  char_length)? _0 initialization?) / (function_name (_0 "*"
                                  _0 char_length)?)
        array_spec              = explicit_shape_spec_list / assumed_shape_spec_list /
                                  deferred_shape_spec_list / assumed_size_spec
        attr_spec               = access_spec / ~"ALLOCATABLE"i / ~"ASYNCHRONOUS"i /
                                  (~"DIMENSION"i "(" array_spec ")") / ~"EXTERNAL"i /
                                  (~"INTENT"i "(" intent_spec ")") / ~"INTRINSIC"i /
                                  language_binding_spec / ~"OPTIONAL"i / ~"PARAMETER"i /
                                  ~"POINTER"i / ~"PROTECTED"i / ~"SAVE"i / ~"TARGET"i /
                                  ~"VALUE"i / ~"VOLATILE"i
        access_spec             = ~"PUBLIC"i / ~"PRIVATE"i
        explicit_shape_spec_list= explicit_shape_spec (_0 "," _0 explicit_shape_spec)*
        explicit_shape_spec     = (_0 lower_bound _0 ":")? _0 upper_bound
        lower_bound             = specification_expr
        upper_bound             = specification_expr
        specification_expr      = scalar_int_expr
        assumed_shape_spec_list = assumed_shape_spec (_0 "," _0 assumed_shape_spec)*
        assumed_shape_spec      = lower_bound? _0 ":"
        deferred_shape_spec_list= deferred_shape_spec (_0 "," _0 deferred_shape_spec)*
        deferred_shape_spec     = ":"
        assumed_size_spec       = (explicit_shape_spec_list _0 ",")? (_0 lower_bound _0
                                  ":")? _0 "*"
        intent_spec             = ~"IN"i / ~"OUT"i / ~"INOUT"i
        language_binding_spec   = ~"BIND"i _0 "(" _0 "C" (_0 "," _0 ~"NAME"i _0 "=" _0
                                  scalar_char_initialization_expr )? _0 ")"
        scalar_char_initialization_expr = char_initialization_expr
        char_initialization_expr= char_expr
        char_expr               = expr
        initialization          = ( "=>" _0 null_init) / initialization_expr
        initialization_expr     = expr
        null_init               = function_reference
        implicit_spec_list      = implicit_spec (_0 "," _0 implicit_spec)*
        implicit_spec           = declaration_type_spec _0 "(" _0 letter_spec_list _0 ")"
        letter_spec_list        = letter_spec (_0 "," _0 letter_spec)*
        letter_spec             = letter (_0 "-" _0 letter )?
        declaration_type_spec   = intrinsic_type_spec / (~"TYPE"i _0 "(" _0 derived_type_spec
                                  _0 ")") / (~"CLASS"i _0 "(" _0 derived_type_spec _0 ")") /
                                  (~"CLASS"i _0 "(" _0 "*" _0 ")")
        intrinsic_type_spec     = (~"INTEGER"i _0 kind_selector?) / (~"REAL"i _0 kind_selector?) /
                                  (~"DOUBLE"i _0 ~"PRECISION"i) / (~"COMPLEX" _0 kind_selector?) /
                                  (~"CHARACTER"i _0 char_selector?) / (~"LOGICAL"i _0 kind_selector?)
        kind_selector           = "(" (_0 ~"KIND"i _0 "=")? _0 scalar_int_initialization_expr _0 ")"
        scalar_int_initialization_expr = expr
        #expr                    = (expr defined_binary_op)? level_5_expr
        expr                    = (level_5_expr _0 defined_binary_op)? _0 level_5_expr
        defined_binary_op       = ~"\.[A-Z][A-Z]*\."i
        level_5_expr            = (equiv_operand _0 equiv_op)? _0 equiv_operand
        equiv_op                = ~"\.EQV\."i / ~"\.NEQV\."i
        equiv_operand           = (or_operand _0 or_op)? _0 or_operand
        or_op                   = ~"\.OR\."i
        or_operand              = (and_operand _0 and_op)? _0 and_operand
        and_op                  = ~"\.AND\."i
        and_operand             = (not_op)? _0 level_4_expr
        not_op                  = ~"\.NOT\."i
        level_4_expr            = (level_3_expr _0 rel_op)? _0 level_3_expr
        level_3_expr            = (level_2_expr _0 concat_op)? _0 level_2_expr
        concat_op               = "//"
        level_2_expr            = (add_operand? _0 add_op)? _0 add_operand
        add_op                  = "+" / "-"
        add_operand             = (mult_operand _0 mult_op)? _0 mult_operand
        mult_op                 = "*" / "/"
        #mult_operand            = level_1_expr (_0 power_op _0 mult_operand)?
        mult_operand            = level_1_expr (_0 power_op _0 level_1_expr)?
        level_1_expr            = (defined_unary_op)? _0 primary
        defined_unary_op        = ~"\.[A-Z][A-Z]*\."i
        primary                 = array_constructor / structure_constructor / function_reference /
                                  type_param_inquiry / designator / constant / type_param_name /
                                  ("(" _0 expr _0 ")")
        constant                = literal_constant / named_constant
        literal_constant        = int_literal_constant / real_literal_constant /
                                  complex_literal_constant / logical_literal_constant /
                                  char_literal_constant / boz_literal_constant
        int_literal_constant    = digit_string ("_" kind_param)?
        digit_string            = ~"[0-9]+"
        kind_param              = digit_string / scalar_int_constant_name
        real_literal_constant   = (significand (exponent_letter exponent)? ("_" kind_param)?) /
                                  (digit_string exponent_letter exponent ("_" kind_param)?)
        significand             = (digit_string "." digit_string?) / ("." digit_string)
        exponent_letter         = ~"[ED]"i
        exponent                = signed_digit_string
        signed_digit_string     = sign? digit_string
        sign                    = "+" / "-"
        complex_literal_constant= "(" _0 real_part _0 "," _0 imag_part _0 ")"
        real_part               = signed_int_literal_constant / signed_real_literal_constant /
                                  named_constant
        imag_part               = signed_int_literal_constant / signed_real_literal_constant /
                                  named_constant
        signed_int_literal_constant = sign? int_literal_constant
        signed_real_literal_constant = sign? real_literal_constant
        logical_literal_constant= (~"\.TRUE\."i ("_" kind_param)?) / (~"\.FALSE\."i
                                  ("_" kind_param)?)
        char_literal_constant   = ((kind_param "_")? _0 "'" _0 rep_char* _0 "'") /
                                  ((kind_param "_")? _0 "\"" _0 rep_char* _0 "\"")
        rep_char                = ~"[^\r\n]+"
        boz_literal_constant    = binary_constant / octal_constant / hex_constant
        binary_constant         = (~"B"i "'" ~"[0-1]+" "'") /  (~"B"i ~"[0-1]+" "\"")
        octal_constant          = (~"O"i "'" ~"[0-7]+" "'") /  (~"O"i "\"" ~"[0-7]+" "\"")
        hex_constant            = (~"Z"i "'" ~"[A-F0-9]+"i "'") /  (~"Z"i "\"" ~"[A-F0-9]+"i "\"")
        designator              = array_section / array_element / structure_component /
                                  substring / object_name
        array_element           = data_ref
        data_ref                = part_ref (_0 "%" _0 part_ref)*
        part_ref                = part_name (_0 "(" _0 section_subscript_list _0 ")")?
        section_subscript_list  = section_subscript ("," section_subscript)*
        section_subscript       = subscript / subscript_triplet / vector_subscript
        subscript               = scalar_int_expr
        scalar_int_expr         = int_expr
        int_expr                = expr
        subscript_triplet       = subscript? ":" subscript? (":" stride)?
        stride                  = scalar_int_expr
        vector_subscript        = int_expr
        array_section           = data_ref (_0 "(" _0 substring_range _0 ")")?
        substring_range         = scalar_int_expr? ":" scalar_int_expr?
        structure_component     = data_ref
        substring               = parent_string _0 "(" _0 substring_range _0 ")"
        parent_string           = array_element / scalar_structure_component / scalar_constant /
                                  scalar_variable_name
        scalar_variable_name    = variable_name
        scalar_structure_component = structure_component
        scalar_constant         = constant
        array_constructor       = ("(/" ac_spec "/)") / ("[" ac_spec "]")
        ac_spec                 = (type_spec "::") / ((type_spec "::")? ac_value_list)
        type_spec               = intrinsic_type_spec / derived_type_spec
        derived_type_spec       = type_name (_0 "(" _0 type_param_spec_list _0 ")")?
        type_param_spec_list    = type_param_spec ("," type_param_spec)*
        type_param_spec         = (keyword "=")? type_param_value
        type_param_value        = "*" / ":" / scalar_int_expr
        ac_value_list           = ac_value ("," ac_value)*
        ac_value                = ac_implied_do / expr
        ac_implied_do           = "(" ac_value_list "," ac_implied_do_control ")"
        ac_implied_do_control   = ac_do_variable "=" scalar_int_expr "," scalar_int_expr (","
                                  scalar_int_expr)?
        ac_do_variable          = scalar_int_variable
        scalar_int_variable     = int_variable
        int_variable            = variable
        variable                = designator
        structure_constructor   = derived_type_spec "(" component_spec_list? ")"
        component_spec_list     = component_spec ("," component_spec)*
        component_spec          = (keyword "=")? component_data_source
        component_data_source   = data_target / proc_target / expr
        data_target             = variable / expr
        proc_target             = proc_component_ref / procedure_name / expr
        proc_component_ref      = variable _0 "%" _0 procedure_component_name
        function_reference      = procedure_designator _0 "(" _0 actual_arg_spec_list? _0 ")"
        procedure_designator    = proc_component_ref / (_0 data_ref _0 "%" _0 binding_name) /
                                  procedure_name
        actual_arg_spec_list    = actual_arg_spec (_0 "," _0 actual_arg_spec)*
        actual_arg_spec         = (keyword _0 "=")? _0 actual_arg
        actual_arg              = proc_component_ref / alt_return_spec / variable /
                                  procedure_name / expr
        alt_return_spec         = "*" _0 label
        label                   = ~"[0-9]{1,5}"
        type_param_inquiry      = designator _0 "%" _0 type_param_name
        power_op                = "**"
        rel_op                  = ~"\.EQ\."i / ~"\.NE\."i / ~"\.LT\."i / ~"\.LE\."i / ~"\.GT\."i /
                                  ~"\.GE\."i / "==" / "/=" / "<" / "<=" / ">" / ">="
        char_selector           = length_selector / ("(" _0 ~"LEN"i _0 "=" _0 type_param_value _0
                                  "," _0 ~"KIND"i _0 "=" _0 scalar_int_initialization_expr _0 ")") /
                                  ("(" _0 type_param_value _0 "," (_0 ~"KIND"i _0 "=")? _0
                                  scalar_int_initialization_expr _0 ")") / ("(" _0 ~"KIND"i _0 "="
                                  _0 scalar_int_initialization_expr (_0 "," _0 ~"LEN"i _0 "=" _0
                                  type_param_value)? _0 ")")
        length_selector         = (_0 "(" (_0 ~"LEN"i "=")? _0 type_param_value _0 ")") /
                                  (_0 "*" _0 char_length _0 ","?)
        char_length             = "(" _0 type_param_value _0 ")"

        ################## names ###################
        program_name            = name
        result_name             = name
        dummy_arg_name          = name
        subroutine_name         = name
        dummy_arg_name          = name
        do_construct_name       = name
        function_name           = name
        named_constant          = name
        scalar_int_constant_name= name
        object_name             = name
        part_name               = name
        variable_name           = name
        type_name               = name
        keyword                 = name
        procedure_name          = name
        procedure_component_name= name
        procedure_name          = name
        binding_name            = name
        type_param_name         = name

        ################## utilities ###################
        _0                      = ~"[ \t]*"
        _1                      = ~"[ \t]+"
        _C                      = _0 "!" ~"[^\n\r]*" EOL
        #_L                      = ~"[^\n\r]*" EOL
        _L                      = _0 EOL
        EOL                     = ~"[\r\n]+"
        blank_line              = ~"[ \t]*[\r\n]"
        # F77 supports through modified _C in every stmts?
    """)

#        bold_text  = bold_open text bold_close
#        text       = ~"[A-Z 0-9]*"i
#        bold_open  = "(("
#        bold_close = "))"

class F2003Visitor(NodeVisitor):
    def generic_visit(self, node, visited_children):
        #import pdb; pdb.set_trace()
        if node.expr_name:
            print(node.expr_name, '---{}---'.format(node.text))

import sys
#import pdb; pdb.set_trace()
sys.setrecursionlimit(1000)
tree = grammar.parse(open('./add.f90', 'r').read())
F2003Visitor().visit(tree)
#print(tree)

