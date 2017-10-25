import os, subprocess
from parsimonious.grammar import Grammar
grammar = Grammar(
    r"""
        program                 = program_unit+
        program_unit            = main_program / external_subprogram / module / block_data
        main_program            = program_stmt? specification_part? execution_part? end_program_stmt
        external_subprogram     = function_subprogram / subroutine_subprogram
        function_subprogram     = function_stmt specification_part? execution_part? internal_subprogram_part? end_function_stmt
        subroutine_subprogram   = subroutine_stmt specification_part? execution_part? internal_subprogram_part? end_subroutine_stmt
        module                  = module_stmt specification_part? module_subprogram_part? end_module_stmt
        block_data              = block_data_stmt specification_part? end_block_data_stmt
        specification_part      = use_stmt* import_stmt* implicit_part* declaration_construct*
        implicit_part           = implicit_part_stmt* implicit_stmt
        implicit_part_stmt      = implicit_stmt / parameter_stmt / format_stmt / entry_stmt
        declaration_construct   = derived_type_def / entry_stmt / enum_def / format_stmt / interface_block / parameter_stmt / procedure_declaration_stmt / specification_stmt / type_declaration_stmt / stmt_function_stmt
        execution_part          = executable_construct execution_part_construct*
        execution_part_construct= executable_construct format_stmt entry_stmt data_stmt
        internal_subprogram_part= contains_stmt internal_subprogram+
        internal_subprogram     = function_subprogram / subroutine_subprogram
        module_subprogram_part  = contains_stmt internal_subprogram+
        module_subprogram       = function_subprogram / subroutine_subprogram
        specification_stmt      = access_stmt / allocatable_stmt / asynchronous_stmt / bind_stmt / common_stmt / data_stmt / dimension_stmt / equivalence_stmt / external_stmt / intent_stmt / intrinsic_stmt / namelist_stmt / optional_stmt / pointer_stmt / protected_stmt / save_stmt / target_stmt / volatile_stmt / value_stmt
        executable_construct    = action_stmt / associate_construct / case_constructor / do_construct / forall_construct / if_construct / select_type_construct / where_construct
        action_stmt             = allocate_stmt / assignment_stmt / backspace_stmt / call_stmt / close_stmt / continue_stmt / cycle_stmt / deallocate_stmt / endfile_stmt / end_function_stmt / end_program_stmt / end_subroutine_stmt / exit_stmt / flush_stmt / forall_stmt / goto_stmt / if_stmt / inquire_stmt / nullify_stmt / open_stmt / pointer_assignment_stmt / print_stmt / read_stmt / return_stmt / rewind_stmt / stop_stmt / wait_stmt / where_stmt / write_stmt / arithmetic_if_stmt / computed_goto_stmt
        program_stmt            = ~"PROGRAM"i program_name
        program_name            = name
        letter                  = ~"[A-Z]"i
        name                    = ~"[A-Z][_A-Z0-9]{0,63}"i



        use_stmt                = "$"
        import_stmt             = "$"
        implicit_stmt           = (~"IMPLICIT"i implicit_spec_list) / (~"IMPLICIT"i ~"NONE"i)
        parameter_stmt          = "$"
        format_stmt             = "$"
        entry_stmt              = "$"
        derived_type_def        = "$"
        enum_def                = "$"
        interface_block         = "$"
        procedure_declaration_stmt  = "$"



        implicit_spec_list      = implicit_spec ("," implicit_spec)*
        implicit_spec           = declaration_type_spec "(" letter_spec_list ")"
        letter_spec_list        = letter_spec ("," letter_spec)*
        letter_spec             = letter ("–" letter )?
        declaration_type_spec   = intrinsic_type_spec / (~"TYPE"i "(" derived_type_spec ")") / (~"CLASS"i "(" derived_type_spec ")") / (~"CLASS"i "(" "*" ")")
        intrinsic_type_spec     = (~"INTEGER"i kind_selector?) / (~"REAL"i kind_selector?) / (~"DOUBLE"i ~"PRECISION"i) / (~"COMPLEX" kind_selector?) / (~"CHARACTER"i char_selector?) / (~"LOGICAL"i kind_selector?)
        kind_selector           = "(" (~"KIND"i "=")? scalar_int_initialization_expr ")"
        scalar_int_initialization_expr = expr
        expr                    = (expr defined_binary_op)? level_5_expr
        defined_binary_op       = ~"\.[A-Z][A-Z]*\."i
        level_5_expr            = (level_5_expr equiv_op)? equiv_operand
        equiv_op                = ~"\.EQV\."i / ~"\.NEQV\."i
        equiv_operand           = (equiv_operand or_op)? or_operand
        or_op                   = ~"\.OR\."i
        or_operand              = (or_operand and_op)? and_operand
        and_op                  = ~"\.AND\."i
        and_operand             = (not_op)? level_4_expr
        not_op                  = ~"\.NOT\."i
        level_4_expr            = (level_3_expr rel_op)? level_3_expr
        level_3_expr            = (level_3_expr concat_op)? level_2_expr
        concat_op               = "//"
        level_2_expr            = (level_2_expr? add_op)? add_operand
        add_op                  = "+" / "-"
        add_operand             = (add_operand mult_op)? mult_operand
        mult_op                 = "*" / "/"
        mult_operand            = level_1_expr (power_op mult_operand)?
        level_1_expr            = (defined_unary_op)? primary
        defined_unary_op        = ~"\.[A-Z][A-Z]*\."i
        primary                 = constant / designator / array_constructor / structure_constructor / function_reference / type_param_inquiry / type_param_name / ("(" expr ")")
        constant                = literal_constant / named_constant
        literal_constant        = int_literal_constant / real_literal_constant / complex_literal_constant / logical_literal_constant / char_literal_constant/ boz_literal_constant
        named_constant          = name
        int_literal_constant    = digit_string kind_param?
    """)

#        bold_text  = bold_open text bold_close
#        text       = ~"[A-Z 0-9]*"i
#        bold_open  = "(("
#        bold_close = "))"

def parse(cup, content, extra):
    #import pdb; pdb.set_trace()
    tree = grammar.parse(content)

#def dump(cup, path, extra):
#    fullpath = os.path.join(path, *extra)
#    if os.path.isfile(fullpath):
#        exts = cup.get_exts_by_file(fullpath)
#        if exts:
#            # TODO: choose one of them
#            fileext, filecup = exts[0]
#            return fileext.dump(filecup, fullpath, [])
#        else:
#            with open(path, 'rb') as f:
#                return cup.write_text(f.read())
#    else:
#        for idx in reversed(range(len(extra))):
#            objpath = os.path.join(path, *extra[:idx+1])
#            remained = extra[idx+1:]
#            if os.path.isfile(objpath):
#                exts = cup.get_exts_by_file(objpath)
#                if exts:
#                    # TODO: choose one of them
#                    fileext, filecup = exts[0]
#                    return fileext.dump(filecup, objpath, remained)
#        return 'file: can not dump {}:{}.'.format(path, extra)
#
#def summary(cup, path, extra):
#    fullpath = os.path.join(path, *extra)
#    if os.path.isfile(fullpath):
#        exts = cup.get_exts_by_file(fullpath)
#        if exts:
#            # TODO: choose one of them
#            fileext, filecup = exts[0]
#            return fileext.summary(filecup, fullpath, [])
#        else:
#            return('{}'.format(subprocess.check_output(["ls", fullpath, "-lrt"]).strip()))
#    else:
#        for idx in reversed(range(len(extra))):
#            objpath = os.path.join(path, *extra[:idx+1])
#            remained = extra[idx+1:]
#            if os.path.isfile(objpath):
#                exts = cup.get_exts_by_file(objpath)
#                if exts:
#                    # TODO: choose one of them
#                    fileext, filecup = exts[0]
#                    return fileext.summary(filecup, objpath, remained)
#        return '{}{}'.format(os.sep, os.sep.join(extra))
